import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# Append the path to the `src` directory
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


from etls.etl_tracks import TracksETL


# Define a function to execute the ETL process
def run_history_etl() -> None:
    etl = TracksETL()
    etl()


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
    "tracks_etl_dag",
    default_args=default_args,
    description="ETL pour écouter l'historique chaque jour",
    schedule_interval=timedelta(days=1),  # Runs daily
    start_date=datetime(2023, 11, 1),
    catchup=False,
) as dag:

    etl_task = PythonOperator(
        task_id="run_history_etl",
        python_callable=run_history_etl,
    )
