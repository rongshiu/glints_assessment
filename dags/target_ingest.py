import pandas as pd
from datetime import datetime
import logging

# create a function for data ingestion pipeline from source db to target db
def target_ingest(sql_path, source_conn, target_conn, target_table_name):
    logger = logging.getLogger()
    try:
        #retrieve query from sql file as per sql_path
        logger.info('Reading SQL file from path')
        query = open(sql_path, 'r')
        logger.info('Read SQL file process completed')

        # get data from source url and store into dataframe df
        logger.info('Getting data from source_db')
        df=pd.read_sql(query.read(), con=source_conn)
        logger.info('Successfully get data from source_db')

        # assign created_at column to indicate datetime of data creation
        df['created_at']=datetime.now()

        logger.info('Uploading data to target_db')
        # upload data into source_db setting if_exist=replace since we do not need to keep history for visualization datamart
        df.to_sql(target_table_name, con=target_conn, index=False, if_exists='replace', method='multi',\
                        chunksize=10000, schema='public')
        logger.info('Successfully uploaded data to target_db')
    except Exception as e:
        logger.error('target_ingest pipeline failed due to {error}',error=e)
