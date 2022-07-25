# Postgres API
from fastapi import FastAPI, Query
from .postgres import db_pipeline

# Test data
db = {'atp_tour' : db_pipeline()}

# Initialise Fast API instance
app = FastAPI()

# Landing Page
@app.get("/")
async def read_root():
    root = {
        'API parameters': {
            'table_name': 'Name of table - only atp_tour at present', 
            'player': 'Names with spaces replaced with underscores - rafael_nadal',
            'tournament': 'Filter for specific tournament', 
            'year_from': 'Integer for starting year (inclusive)',
            'year_to': 'Integer for ending year (inclusive)',
            'col': 'name of column to pull through - each entered separately',
            }, 
        'Tables': {k: list(v.columns) for k, v in db.items()},
        }

    return root
# Get request
@app.get("/{table_name}/")
async def read_item(table_name: str, player: str = Query(default=None), year_from: int = Query(default=None), year_to: int = Query(default=None), col: list[str] = Query(default=None), tournament: str = Query(default=None), ):  
    # Select table
    table = db[table_name]
    
    # Filter for year
    if year_from != None:
        table = table[table['tourney_date'].dt.year >= year_from].copy()

    if year_to != None:
        table = table[table['tourney_date'].dt.year <= year_to].copy()

    # Filter for tournament
    if tournament != None:
        tournament = tournament.replace('_', ' ').replace('+', ' ').title()
        table['tourney_name'] = [i.replace("'", '') for i in table['tourney_name']]
        table = table[table['tourney_name'] == tournament].copy()

    # Filter for player
    if player != None:
        player = player.replace('_', ' ').replace('+', ' ').title()
        table = table[(table['winner_name'] == player) | (table['loser_name'] == player)].copy()

    # Filter for cols
    if col != None:
        table = table[col].copy() 

    return table.to_json()