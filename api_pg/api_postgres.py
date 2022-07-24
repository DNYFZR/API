# Postgres API
import pandas as pd, psycopg2 as sql
from fastapi import FastAPI, Query
from sqlalchemy import create_engine

# Database extract pipeline - function works outside Docker system
def db_pipeline(db = 'ATP_tour_data', user = 'postgres', pw = 'postgres', query = '''SELECT * FROM "matches";'''):
    # Set up engine
    engine = create_engine(f'postgresql+psycopg2://{user}:{pw}@localhost:5432/{db}')
    
    # Set up connection
    conn = sql.connect(dbname = db, user = user, password = f'{pw}')
    cur = conn.cursor()

    # Execute & fetch data
    cur.execute(query)
    
    column_names = [desc[0] for desc in cur.description]
    output = []
    for row in cur:
        output.append(row)
    
    # Close connection & return output
    conn.close()
    return pd.DataFrame(output, columns=column_names)

# Test data
atp_tour = db_pipeline()
db = {'atp_tour' : atp_tour}

# Initialise Fast API instance
app = FastAPI()

# API Build

# Base URL with DB table info
@app.get("/")
async def read_root():
    return {k: list(v.columns) for k, v in db.items()}

# Get request
@app.get("/{table_name}/")
async def read_item(table_name: str, player: str = Query(default=None), year: int = Query(default=None), col: list[str] = Query(default=None)):  
    # Select table
    table = db[table_name]
    
    # Filter for year
    if year != None:
        table = table[table['tourney_date'].dt.year == year].copy()

    # Filter for player
    if player != None:
        player = player.replace('_', ' ').replace('+', ' ').replace('&', ' ').title()
        table = table[(table['winner_name'] == player) | (table['loser_name'] == player)].copy()

    # Filter for cols
    if col != None:
        table = table[col].copy() 

    return table.to_json()