from fastapi import FastAPI, Query
from .query import generate_query
from .database import pipeline

########### API Build ###########
api = FastAPI()

# API base page
@api.get('/')
def home():
    return '''API Homepage...'''

# Database get request
@api.get('/{db}')
def get_request(db: str, table: str, 
    select_col: list[str] = Query(default= None), 
    date_col: str = Query(default= None), 
    date_from: str = Query(default= None), 
    date_to: str = Query(default= None),
    tournament_col: str = Query(default= None),  
    tournament: str = Query(default= None),
    player_col: list[str] = Query(default= None),  
    player: str = Query(default= None), 
    ):

    '''
        Builds CTEs for specified parameters and created query string for SQL Alchemy engine.
        Then runs the query on selected database table.
        Returns a JSON / Python dictionary object.
    '''
    q =  generate_query(
        table=table, 
        select_col=select_col, 
        date_col=date_col, date_from=date_from, date_to=date_to, 
        tournament_col=tournament_col, tournament=tournament, 
        player_col=player_col, player=player)
    
    return pipeline(query = q, db = db)