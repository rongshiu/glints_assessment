Objective:
This project sets up the below services in a docker container
- airflow webserver
- airflow postgres
- postgres (source_db)
- postgres (target_db)

This repo consists of the below files/folders:
- docker-compose.yml:
    - docker compose yml which brings up all the services
- dockerfile:
    - instructions of flow to create image to be use by airflow service
- requirements.txt:
    - dependencies to be installed via dockerfile instructions
- .env
    - env file storing variables for docker compose setup

Requirement to begin:
- you will need to have docker installed to begin, you may download docker desktop from https://www.docker.com/products/docker-desktop/

Command to start:
- docker compose up -d

Command to bring down all containers:
- docker compose down

How to use:
- Pipeline are schedule of airflow and this can be monitored via localhost:5884

Thought Process:
- DAG Setup:
    - 2 DAGs source_ingest_dag and target_ingest_dag are created.
        * Steps 3,4 specified that 2 separate dags needs to be setup. One for data ingestion from source (url given) to postgres (source_db) and another one to create datamart for analytics purposes on another postgres (target_db).
    - An external task sensor is setup within target_ingest_dag to poke for the source_ingest task completion before starting.
        * Step 5 requires target_ingest_dag to run only after source_ingest_dag tasks are completed. A timedelta arg of 5min is added because the dags are scheduled at different time
    - Scheduled source_ingest_dag to run weekly at hour 0 min 0 every Sunday and target_ingest_dag to run weekly at hour 0 min 5 every Sunday
        * Step 6 requires dag to be schedule on weekly basis
    - I have created a secrets_management.py file for storing temp secrets since we are only doing a local setup. This should be maintain in aws secrets manager in production env
- Source DB ingestion
    - added created_at timestamp column prior ingestion
    * designed data ingestion appending data on each run rather than a full refresh, this allows us to trace back historical data
- Target DB ingestion
    - added created_at timestamp column prior ingestion
    * allows us to keep track of last refresh timestamp
    - created 4 datamarts for 4 different analytics use case
    * I have decided to create 4 datamarts for 4 different use cases as specified in step 2, this could improve load time by having minimal data transformation on visualization tool

Services Credentials:

- Service: airflow
    * username: airflow
    * password: airflow123
    * local port: 5884

- Service: source_db (postgres)
    * username: source_db
    * username: source_db
    * host: source_db
    * local port: 5432                       
    * db: source_db

- Service: target_db (postgres)
    * username: target_db
    * username: target_db
    * host: target_db
    * local port: 5433                      
    * db: target_db

- Service: airflow (postgres)
    * username: airflow
    * username: airflow
    * host: postgres
    * local port: 5434                 
    * db: airflow