FROM apache/airflow:2.3.0
COPY requirements.txt .
RUN pip install -r requirements.txt
# USER airflow
# RUN airflow variables set airflow_db_conn \
#     postgresql://airflow:airflow@localhost:5434/airflow \
#     && airflow variables set source_db_conn \
#     postgresql://source_db:source_db@localhost:5432/source_db  \
#     && airflow variables set target_db_conn \
#     postgresql://target_db:target_db@localhost:5433/target_db
# USER root