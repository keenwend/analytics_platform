from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import zipfile
import os

SUPERSET_CONTAINER = "analytics-platform-superset-1"
EXPORT_DIR = "/app/superset_exports"

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def unzip_exports():
    exports = [
        ("/opt/airflow/superset_exports/dashboards.zip", "/opt/airflow/superset_exports/dashboards/"),
        ("/opt/airflow/superset_exports/datasources.zip", "/opt/airflow/superset_exports/datasources/"),
    ]
    for zip_path, extract_to in exports:
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_to)
        print(f"Extracted {zip_path} → {extract_to}")

with DAG(
    dag_id="superset_export",
    default_args=default_args,
    schedule_interval="0 2 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["superset"],
) as dag:

    export_dashboards = BashOperator(
        task_id="export_dashboards",
        bash_command=f"docker exec {SUPERSET_CONTAINER} superset export-dashboards -f {EXPORT_DIR}/dashboards.zip",
    )

    export_datasources = BashOperator(
        task_id="export_datasources",
        bash_command=f"docker exec {SUPERSET_CONTAINER} superset export-datasources -f {EXPORT_DIR}/datasources.zip",
    )

    unzip_exports_task = PythonOperator(
        task_id="unzip_exports",
        python_callable=unzip_exports,
    )

export_dashboards >> export_datasources >> unzip_exports_task