from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import psycopg2
import sys

sys.path.insert(0, "/opt/airflow/tasks")
from extract_rates import extract_exchange_rates
from load_to_postgres import load_rates
from trigger_dbt import run_dbt

default_args = {
    "owner": "data-engineer",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

def extract_and_load():
    data = extract_exchange_rates()
    conn = psycopg2.connect(
        dbname="rates_db", user="admin", password="password", host="postgres"
    )
    load_rates(conn, data)

with DAG(
    "exchange_rate_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    tags=["finance", "kes"],
) as dag:

    extract_load = PythonOperator(
        task_id="extract_and_load",
        python_callable=extract_and_load,
    )

    transform = PythonOperator(
        task_id="run_dbt_transforms",
        python_callable=run_dbt,
    )

    extract_load >> transform
