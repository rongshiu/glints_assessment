from datetime import timedelta
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from target_ingest import target_ingest
from secrets_management import get_source_db_conn,get_target_db_conn

#get secrets
# this is only for local setup usage
## This should be maintain in aws secrets manager in production env
source_db_conn=get_source_db_conn
target_db_conn=get_target_db_conn

default_args = {
    'owner': 'rongshiu@gmail.com',
    'depends_on_past': False,
    'start_date': '2022-10-22',
    'email': ['rongshiu@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1
}

target_ingest_dag = DAG(
    tags=['target_ingest'],
    dag_id='target_ingest_dag',
    default_args=default_args,
    description='dag created to schedule target data ingestion pipeline',
    schedule_interval='5 * * * *', #runs at hour 0 min 5 every Sunday
    catchup=False
)

start = DummyOperator(
    task_id='start',
    dag=target_ingest_dag
)

target_ingestion_task_2a = PythonOperator(
    task_id = 'target_ingestion_task_2a',
    python_callable = target_ingest,
    dag=target_ingest_dag,
    op_kwargs={'sql_path': './dags/2a.sql', 'source_conn': source_db_conn, 'target_conn': target_db_conn, 'target_table_name': 'datamart_2a'}
)

target_ingestion_task_2b = PythonOperator(
    task_id = 'target_ingestion_task_2b',
    python_callable = target_ingest,
    dag=target_ingest_dag,
    op_kwargs={'sql_path': './dags/2b.sql', 'source_conn': source_db_conn, 'target_conn': target_db_conn, 'target_table_name': 'datamart_2b'}
)

target_ingestion_task_2c = PythonOperator(
    task_id = 'target_ingestion_task_2c',
    python_callable = target_ingest,
    dag=target_ingest_dag,
    op_kwargs={'sql_path': './dags/2c.sql', 'source_conn': source_db_conn, 'target_conn': target_db_conn, 'target_table_name': 'datamart_2c'}
)

target_ingestion_task_2d = PythonOperator(
    task_id = 'target_ingestion_task_2d',
    python_callable = target_ingest,
    dag=target_ingest_dag,
    op_kwargs={'sql_path': './dags/2d.sql', 'source_conn': source_db_conn, 'target_conn': target_db_conn, 'target_table_name': 'datamart_2d'}
)

source_ingest_sensor=ExternalTaskSensor(
    timeout=900,
    dag=target_ingest_dag,
    task_id='source_ingest_sensor',
    task_concurrency=1,
    depends_on_past=False,
    email=['rongshiu@gmail.com'],
    external_task_id='source_ingestion_task',
    external_dag_id='source_ingest_dag',
    execution_delta=timedelta(minutes=5)
)

start >> source_ingest_sensor >> [target_ingestion_task_2a, target_ingestion_task_2b, target_ingestion_task_2c, target_ingestion_task_2d]
