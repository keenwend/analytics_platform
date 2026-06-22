from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

with DAG(
    dag_id="test_pipeline",
    start_date=datetime(2025,1,1),
    schedule="@daily",
    catchup=False
):

    task = BashOperator(
        task_id="hello",
        bash_command="echo hello"
    )

    task = BashOperator(
        task_id="dbt_run",
        cwd="/opt/airflow/dbt/dbt_project",
        bash_command="""
        dbt debug --profiles-dir /opt/airflow/dbt
        dbt run --profiles-dir /opt/airflow/dbt
        """
    )

    task = BashOperator(
        task_id="inspect_dbt",
        bash_command="""
        whoami
        pwd
    
        echo "=== DBT DIR ==="
        ls -la /opt/airflow/dbt
    
        echo "=== PROJECT DIR ==="
        ls -la /opt/airflow/dbt/dbt_project
    
        echo "=== FIND PROFILES ==="
        find /opt/airflow -name profiles.yml 2>/dev/null
    
        echo "=== FIND DBT PROJECT ==="
        find /opt/airflow -name dbt_project.yml 2>/dev/null
        """
    )