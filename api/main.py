from fastapi import FastAPI
import datetime as dt, pandas as pd

# Initialise Fast API instance
app = FastAPI()

# Test data
atp_tour = pd.read_csv(r'/api/data/ATP_tour.csv', index_col=0, parse_dates=['tourney_date'])

db = {'atp_tour' : atp_tour}

# API Build

# Base URL
@app.get("/")
async def read_root():
    return f"API status 200 {dt.datetime.strftime(dt.date.today(), '%H:%M on %d-%b-%Y')}"

# Get request
@app.get("/tables/{table_name}/{player}")
async def read_item(table_name: str, player: str):  
    # Select table
    table = db[table_name]
    
    # Filter for player
    if player != None:
        player = player.replace('_', ' ').title()
        table = table[(table['winner_name'] == player) | (table['loser_name'] == player)].copy()

    return table.to_json()