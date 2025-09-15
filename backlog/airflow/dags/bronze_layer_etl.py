from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.sensors.glue import GlueJobSensor

default_args = {
    'owner': 'iesb-bigdata',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'bronze_layer_etl',
    default_args=default_args,
    description='IESB BigData Bronze Layer ETL Pipeline',
    schedule_interval='@daily',
    catchup=False,
    tags=['iesb', 'bigdata', 'bronze', 'etl']
)

# Run Bronze Layer ETL Glue Job
run_bronze_etl = GlueJobOperator(
    task_id='run_bronze_layer_etl',
    job_name='iesb-bronze-layer-etl',
    script_location='s3://iesb-bigdata/scripts/bronze-layer-etl.py',
    s3_bucket='iesb-bigdata',
    iam_role_name='iesb-glue-service-role',
    create_job_kwargs={
        'GlueVersion': '4.0',
        'NumberOfWorkers': 2,
        'WorkerType': 'G.1X',
        'Timeout': 60,
        'MaxRetries': 0
    },
    dag=dag
)

# Wait for job completion
wait_for_bronze_etl = GlueJobSensor(
    task_id='wait_for_bronze_etl_completion',
    job_name='iesb-bronze-layer-etl',
    run_id="{{ task_instance.xcom_pull(task_ids='run_bronze_layer_etl', key='return_value') }}",
    timeout=3600,
    poke_interval=60,
    dag=dag
)

# Run S3 Crawler after ETL
run_s3_crawler = GlueJobOperator(
    task_id='run_s3_crawler',
    job_name='iesb-s3-crawler-trigger',
    script_location='s3://iesb-bigdata/scripts/trigger_crawler.py',
    s3_bucket='iesb-bigdata',
    iam_role_name='iesb-glue-service-role',
    create_job_kwargs={
        'GlueVersion': '4.0',
        'NumberOfWorkers': 1,
        'WorkerType': 'G.1X',
        'Timeout': 30,
        'MaxRetries': 0
    },
    dag=dag
)

# Set task dependencies
run_bronze_etl >> wait_for_bronze_etl >> run_s3_crawler
