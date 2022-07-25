# Postgres API
import pandas as pd
from fastapi import FastAPI, Query
from .postgres import db_pipeline

# Test data
db = {'atp_tour' : db_pipeline()}

# Initialise Fast API instance
app = FastAPI()

# Landing Page
@app.get("/")
async def read_root():
    return {k: list(v.columns) for k, v in db.items()}

# Get request
@app.get("/{table_name}/")
async def read_item(table_name: str, player: str = Query(default=None), year: int = Query(default=None), col: list[str] = Query(default=None), winner: str = Query(default=None), ):  
    # Select table
    table = db[table_name]
    
    # Filter for year
    if year != None:
        table = table[table['tourney_date'].dt.year == year].copy()

    # Filter for winner
    if winner != None:
        winner = winner.replace('_', ' ').replace('+', ' ').title()
        table = table[table['winner_name'] == winner].copy()

    # Filter for player
    if player != None and winner == None:
        player = player.replace('_', ' ').replace('+', ' ').title()
        table = table[(table['winner_name'] == player) | (table['loser_name'] == player)].copy()

    # Filter for cols
    if col != None:
        table = table[col].copy() 

    return table.to_json()