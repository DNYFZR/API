import pandas as pd, psycopg2 as sql

# Database extract pipeline - function works outside Docker system
def db_pipeline(db = 'ATP_tour_data', user = 'postgres', pw = 'Nadal22', query = '''SELECT * FROM "matches";'''):  
    # Set up connection
    conn = sql.connect(host = 'host.docker.internal', database = db, user = user, password = f'{pw}')
    cur = conn.cursor()

    # Execute & fetch data
    cur.execute(query)
    
    column_names = [desc[0] for desc in cur.description]
    output = [row for row in cur]
    
    # Close connection & return output
    conn.close()
    output = pd.DataFrame(output, columns=column_names)
    output['tourney_date'] = pd.to_datetime(output['tourney_date'])

    return output
