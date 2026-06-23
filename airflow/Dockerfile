FROM apache/airflow:2.10.5

RUN apt-get install -y --no-install-recommends unzip

RUN pip install --no-cache-dir \
    dbt-core \
    dbt-postgres \
    great-expectations \
    psycopg2-binary \
    kafka-python==2.0.2 \
    minio==7.2.7 \
    pandas==2.2.2 \
    docker==7.0.0