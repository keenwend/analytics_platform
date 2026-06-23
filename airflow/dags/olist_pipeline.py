from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pandas as pd
import psycopg2
from minio import Minio
from io import BytesIO

MINIO_ENDPOINT = "minio:9000"
MINIO_ACCESS   = "minio"
MINIO_SECRET   = "minio123"
BUCKET         = "raw-data"

PG_CONN = {
    "host": "postgres",
    "dbname": "analytics",
    "user": "admin",
    "password": "admin"
}

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}


def load_csv_from_minio(filename: str, table: str, schema: str = "raw"):
    client = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS,
                   secret_key=MINIO_SECRET, secure=False)
    obj = client.get_object(BUCKET, filename)
    df = pd.read_csv(BytesIO(obj.read()))

    df = df.where(pd.notnull(df), None)

    conn = psycopg2.connect(**PG_CONN)
    cur = conn.cursor()
    cur.execute(f"TRUNCATE TABLE {schema}.{table}")

    cols = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))
    for row in df.itertuples(index=False, name=None):
        cur.execute(
            f"INSERT INTO {schema}.{table} ({cols}) VALUES ({placeholders})",
            row
        )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {len(df)} rows into {schema}.{table}")


with DAG(
    dag_id="olist_etl_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["olist", "etl"],
) as dag:

    load_orders = PythonOperator(
        task_id="load_orders",
        python_callable=load_csv_from_minio,
        op_kwargs={
            "filename": "olist_orders_dataset.csv",
            "table": "orders",
        },
    )

    load_items = PythonOperator(
        task_id="load_order_items",
        python_callable=load_csv_from_minio,
        op_kwargs={
            "filename": "olist_order_items_dataset.csv",
            "table": "order_items",
        },
    )

    run_dbt = BashOperator(
        task_id="dbt_run",
        cwd="/opt/airflow/dbt/dbt_project",
        bash_command="dbt run --profiles-dir /opt/airflow/dbt",
    )

    test_dbt = BashOperator(
        task_id="dbt_test",
        cwd="/opt/airflow/dbt/dbt_project",
        bash_command="dbt run --profiles-dir /opt/airflow/dbt",
    )

    [load_orders, load_items] >> run_dbt >> test_dbt
