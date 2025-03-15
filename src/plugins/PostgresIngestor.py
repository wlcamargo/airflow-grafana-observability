import duckdb
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from observability.console_logger import ConsoleLogger
from observability.tracer import TelemetryTracer


class DataIngestionTool:
    def __init__(self, source_config, target_config, app_name):
        """
        Initializes the DataIngestionTool with source and target configurations.
        """
        self.logger = ConsoleLogger(
            otlp_endpoint="http://172.18.206.109:4317", app_name=app_name
        )
        self.tracer = TelemetryTracer()
        self.tracer.setup(
            otlp_endpoint="http://172.18.206.109:4317", app_name=app_name
        )

        self.source_config = source_config
        self.target_config = target_config
        self.duckdb_conn = duckdb.connect(":memory:")

    def get_postgres_connection(self, config):
        """Establishes a connection to PostgreSQL using the provided configuration."""
        return psycopg2.connect(
            dbname=config["dbname"],
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"]
        )

    def extract_from_source(self, query, table_name):
        """Extracts data from the source PostgreSQL database."""
        with self.tracer.start_span(f"extract_from_source_{table_name}"):
            self.logger.info(f"Extracting data from source table '{table_name}'...")
            with self.get_postgres_connection(self.source_config) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
            self.logger.info(f"Extracted {len(rows)} rows from '{table_name}'.")
            return rows

    def transform_data(self, data, table_name):
        """Transforms the extracted data using DuckDB."""
        with self.tracer.start_span(f"transform_data_{table_name}"):
            self.logger.info(f"Transforming data for table '{table_name}' using DuckDB...")
            df = pd.DataFrame(data)
            self.duckdb_conn.register("source_data", df)
            transformed_data = self.duckdb_conn.execute("SELECT * FROM source_data").fetchall()
            columns = [col[0] for col in self.duckdb_conn.execute("DESCRIBE source_data").fetchall()]
            transformed_data_dict = [dict(zip(columns, row)) for row in transformed_data]
            self.logger.info(f"Data transformation complete for table '{table_name}'.")
            return transformed_data_dict

    def load_to_target(self, table_name, data):
        """Loads the transformed data into the target PostgreSQL database."""
        with self.tracer.start_span(f"load_to_target_{table_name}"):
            if not data:
                self.logger.warning(f"No data to load into '{table_name}'. Skipping.")
                return

            self.logger.info(f"Loading data into target table '{table_name}'...")
            with self.get_postgres_connection(self.target_config) as conn:
                with conn.cursor() as cursor:
                    columns = data[0].keys()
                    placeholders = ", ".join(["%s"] * len(columns))
                    insert_query = f"""
                        INSERT INTO {table_name} ({', '.join(columns)})
                        VALUES ({placeholders});
                    """
                    cursor.executemany(insert_query, [list(row.values()) for row in data])
                conn.commit()
            self.logger.info(f"Loaded {len(data)} rows into '{table_name}'.")

    def truncate_target_table(self, table_name):
        """Truncates the target table, removing all existing rows."""
        with self.tracer.start_span(f"truncate_table_{table_name}"):
            self.logger.info(f"Truncating target table '{table_name}'...")
            with self.get_postgres_connection(self.target_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"TRUNCATE TABLE {table_name};")
                conn.commit()
            self.logger.info(f"Truncated table '{table_name}'.")

    def run(self, source_queries_to_tables):
        """Orchestrates the ETL process for multiple tables."""
        for query, target_table in source_queries_to_tables.items():
            with self.tracer.start_span(f"run_etl_process_{target_table}"):
                self.logger.info(f"Starting ETL process for table '{target_table}'...")

                # Step 1: Truncate the target table
                self.truncate_target_table(target_table)

                # Step 2: Extract data from the source
                data = self.extract_from_source(query, target_table)

                if not data:
                    self.logger.warning(f"No data extracted for '{target_table}'. Skipping transformation and load.")
                    continue

                # Step 3: Transform the data
                transformed_data = self.transform_data(data, target_table)

                # Step 4: Load the transformed data into the target
                self.load_to_target(target_table, transformed_data)

                self.logger.info(f"ETL process completed for table '{target_table}'.")
