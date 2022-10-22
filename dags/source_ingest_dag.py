from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from source_ingest import source_ingest
from secrets_management import get_source_db_conn

# get secrets
# this is only for local setup usage
## This should be maintain in aws secrets manager in production env
source_db_conn=get_source_db_conn()

default_args = {
    'owner': 'rongshiu@gmail.com',
    'depends_on_past': False,
    'start_date': '2022-10-22',
    'email': ['rongshiu@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1
}

source_ingest_dag = DAG(
    tags=['source_ingest'],
    dag_id='source_ingest_dag',
    default_args=default_args,
    description='dag created to schedule source data ingestion pipeline',
    schedule_interval='0 0 * * 0', #runs at hour 0 every Sunday
    catchup=False
)

start = DummyOperator(
    task_id='start',
    dag=source_ingest_dag
)

source_ingestion_task = PythonOperator(
    task_id = 'source_ingestion_task',
    python_callable = source_ingest,
    dag=source_ingest_dag,
    op_kwargs={'conn': source_db_conn}
)

start >> source_ingestion_task
