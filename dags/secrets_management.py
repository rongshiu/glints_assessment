# this is only for local setup usage
## This should be maintain in aws secrets manager in production env
def get_source_db_conn():
    source_db_conn="postgresql://{u}:{p}@{h}:{port}/{db}".\
                        format(u='source_db',
                        p='source_db',
                        h='source_db',
                        port=5432,
                        db='source_db')
    return source_db_conn

def get_target_db_conn():
    target_db_conn="postgresql://{u}:{p}@{h}:{port}/{db}".\
                        format(u='target_db',
                        p='target_db',
                        h='target_db',
                        port=5432,
                        db='target_db')
    return target_db_conn