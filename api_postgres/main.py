import pandas as pd
from sqlalchemy import create_engine, text
from fastapi import FastAPI, Query

########### Database Engine ###########

# Create Engine - host name for local DB use with Docker contianer
def init_engine(db = 'ATP_tour_data', user:str = 'postgres', pw:str = 'Nadal22', server:str = 'host.docker.internal:5432'):
    
    conn_str = f'postgresql+psycopg2://{user}:{pw}@{server}/{db}'
    return create_engine(conn_str) 


########### API Build ###########
api = FastAPI()

# Home
@api.get('/')
def home():
    return '''API Homepage...'''

# Get request
@api.get('/{db}')
def get(db: str, table: str, select_col: list[str] = Query(default= None), ):
    '''
        Run query on selected table and return dataframe.
    '''
    # Build query
    query = f'''SELECT * FROM {table} ;'''
    
    if select_col != None:
        if len(select_col) == 1:
            query = query.replace('*', select_col[0])
        else:
            query = query.replace('*', ', '.join(select_col).lstrip(', '))

    # Run query
    engine = init_engine(db=db)
    with engine.connect() as cursor:
        raw = cursor.execute(text(query))
        column_names = [col for col in raw.keys()]
        output = [row for row in raw]

    return pd.DataFrame(data=output, columns=column_names).to_json()
