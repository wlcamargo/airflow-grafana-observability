from plugins.PostgresIngestor import DataIngestionTool
from configs.configs import source_db_config, target_db_config
from configs.tables import source_queries_to_tables
from observability.console_logger import ConsoleLogger
from observability.tracer import TelemetryTracer

if __name__ == "__main__":
    logger = ConsoleLogger(
        otlp_endpoint="http://172.18.206.109:4317", app_name="postgress_ingestor"
    )
    tracer = TelemetryTracer()
    tracer.setup(
        otlp_endpoint="http://172.18.206.109:4317", app_name="postgress_ingestor"
    )

    #####################################################
    # Process data
    #####################################################
    logger.info("starting ETL process...")
    etl_tool = DataIngestionTool(source_db_config, target_db_config, app_name="postgress_ingestor")
    etl_tool.run(source_queries_to_tables)
    try:
        etl_tool.run(source_queries_to_tables)
        logger.info("ETL process completed successfully.")
    except Exception as e:
        logger.error(f"ETL process failed: {e}")
        exit(1)
