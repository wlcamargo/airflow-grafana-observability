from datetime import datetime
from airflow import DAG
from common.create_docker_task import create_docker_task

default_args = {
    "owner": "Wallace Camargo",
    "depends_on_past": False,
}

with DAG(
    dag_id="python-ingestor-postgres",
    default_args=default_args,
    start_date=datetime(2025, 3, 15),
    schedule_interval="@once", 
    catchup=False,
    tags=["python", "ingestion", "postgres"],
) as dag:
    
    run_ingestion = create_docker_task(
        task_id="run_ingestion",
        image="python-ingestor-postgres",
        command="python3 main.py"
    )

    run_ingestion
