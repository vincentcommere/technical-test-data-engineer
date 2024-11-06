import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# Append the path to the `src` directory
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from src.etls.etl_users import UsersETL

etl = UsersETL()


# Define functions to execute each part of the ETL process
def run_etl_first_task() -> None:
    etl.extract()


def run_etl_second_task() -> None:
    etl.transform()


def run_etl_third_task() -> None:
    etl.load()


# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    "users_etl_dag",
    default_args=default_args,
    description="ETL pour écouter l'historique chaque jour",
    schedule_interval=timedelta(days=1),  # Runs daily
    start_date=datetime(2023, 11, 1),
    catchup=False,
) as dag:

    etl_first_task = PythonOperator(
        task_id="run_etl_first_task", python_callable=run_etl_first_task
    )

    etl_second_task = PythonOperator(
        task_id="run_etl_second_task", python_callable=run_etl_second_task
    )

    etl_third_task = PythonOperator(
        task_id="run_etl_third_task", python_callable=run_etl_third_task
    )

    # Set task dependencies
    etl_first_task >> etl_second_task >> etl_third_task
