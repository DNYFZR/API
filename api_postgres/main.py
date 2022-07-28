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
def get(
    db: str, 
    table: str, 
    select_col: list[str] = Query(default= None), 
    date_col: str = Query(default= None), 
    date_from: str = Query(default= None), 
    date_to: str = Query(default= None),
    tournament_col: str = Query(default= None),  
    tournament: str = Query(default= None), 
    ):

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

    ### CTE's ###

    # Date fiter as CTE
    if date_col != None and (date_from != None or date_to != None):
     
        if date_to == None:
            cte = f'''WITH temp_table as (SELECT * FROM {table} WHERE EXTRACT(YEAR from {date_col}::DATE) >= {date_from})'''
     
        elif date_from == None:
            cte = f'''WITH temp_table as (SELECT * FROM {table} WHERE EXTRACT(YEAR from {date_col}::DATE) <= {date_to})'''
     
        else:
            cte = f'''WITH temp_table as (SELECT * FROM {table} WHERE EXTRACT(YEAR from {date_col}::DATE) >= {date_from} AND EXTRACT(YEAR from {date_col}::DATE) <= {date_to} )'''
     
        query = f'''{cte} {query.replace(table, 'temp_table')}'''

    # Tournament filter as CTE
    if tournament_col != None and tournament != None:
        tournament = f''' '{tournament.replace('_', ' ').title()}' '''

        if date_col == None:
            cte = f'''WITH temp_table as (SELECT * FROM {table} WHERE {tournament_col} = {tournament})'''
            query = f'''{cte} {query.replace(table, 'temp_table')}'''

        else:
            cte_1 = f''', temp_table_2 as (SELECT * FROM temp_table WHERE {tournament_col} = {tournament})'''
            cte_0, query = query.rsplit('SELECT', maxsplit=1)
            query = f'''{cte_0} {cte_1} SELECT {query.replace('temp_table', 'temp_table_2')}'''
     
    # Run query
    engine = init_engine(db=db)
    with engine.connect() as cursor:
        raw = cursor.execute(text(query))
        column_names = [col for col in raw.keys()]
        output = [row for row in raw]

    return {col : [i[n] for i in output] for n, col in enumerate(column_names)}
