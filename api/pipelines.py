# Database Connection Pipelines
import pandas as pd, pyodbc as azure_sql, psycopg2 as postgres_sql

# Postgres Database Pipeline
def postgres_pipeline(db = 'ATP_tour_data', user = 'postgres', pw = 'Nadal22', query = '''SELECT * FROM "matches";'''):  
    
    # Set up connection
    conn = postgres_sql.connect(host = 'host.docker.internal', database = db, user = user, password = f'{pw}')
    cur = conn.cursor()

    # Execute & fetch data
    cur.execute(query)
    column_names = [desc[0] for desc in cur.description]
    output = [row for row in cur]
    conn.close()
    
    # Combined & format output
    output = pd.DataFrame(output, columns=column_names)
    output['tourney_date'] = pd.to_datetime(output['tourney_date'])

    return output


# SQL Server (Azure) Database Pipeline
def azure_pipeline(server = '<server>.database.windows.net', database = '<database>', username = '<username>', password = '{<password>}', driver= '{ODBC Driver 17 for SQL Server}'):  
    
    # Set up connection
    conn = azure_sql.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 
    cur = conn.cursor()
    
    # Execute & fetch
    cur.execute("SELECT * FROM sys.databases")       
    column_names = [desc[0] for desc in cur.description]
    output = [row for row in cur]
    conn.close()

    # Comibne & format output
    output = pd.DataFrame(output, columns=column_names)
    output['tourney_date'] = pd.to_datetime(output['tourney_date'])

    return output

