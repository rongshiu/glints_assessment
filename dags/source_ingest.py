import pandas as pd
from datetime import datetime
import logging

# create a function for data ingestion pipeline from source
def source_ingest(conn):
    logger = logging.getLogger()
    try:
        logger.info('Getting source data')
        # get data from source url and store into dataframe df
        url="https://healthdata.gov/api/views/aitj-yx37/rows.csv?accessType=DOWNLOAD"
        df=pd.read_csv(url)
        logger.info('Successfully get source data')
        # standardize column naming convention
        # remove trailing and preceeding spaces, naming to lowercase and replacing empty spaces with underscore
        df.columns= [col.strip().lower().replace(' ','_') for col in df.columns]
        # assign created_at column to indicate datetime of data creation
        df['created_at']=datetime.now()
        logger.info('Uploading source data')
        # upload data into source_db
        df.to_sql('source_table', con=conn, index=False, if_exists='append', method='multi',\
                        chunksize=10000, schema='public')
        logger.info('Successfully uploaded source data')
    except Exception as e:
        logger.error('source_ingest pipeline failed due to {error}',error=e)
