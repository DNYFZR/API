from fastapi import FastAPI, Query
from typing import Union
import datetime as dt, pandas as pd

# Initialise Fast API instance
app = FastAPI()

# Test data
atp_tour = pd.read_csv(r'/api/data/ATP_tour.csv', index_col=0, parse_dates=['tourney_date'])

db = {'atp_tour' : atp_tour}

# API Build

# Base URL with DB table info
@app.get("/")
async def read_root():
    return {k: list(v.columns) for k, v in db.items()}

# Get request
@app.get("/{table_name}/{player}")
async def read_item(table_name: str, player: str, year: int = Query(default=None), col: list[str] = Query(default=None)):  
    # Select table
    table = db[table_name]
    
    # Filter for year
    if year != None:
        table = table[table['tourney_date'].dt.year == year].copy()

    # Filter for player
    if player != None:
        player = player.replace('_', ' ').title()
        table = table[(table['winner_name'] == player) | (table['loser_name'] == player)].copy()

    # Filter for cols
    if col != None:
        table = table[col].copy() 

    return table.to_json()