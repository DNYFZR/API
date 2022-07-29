from sqlalchemy import create_engine, text 
from sqlalchemy.engine import URL

# Create Engine - default host name for local DB use within Docker contianer
def pipeline(
    query:str, db = 'ATP_tour_data', user:str = 'postgres', pw:str = 'Nadal22', 
    server:str = 'host.docker.internal', port:int = 5432, db_type:str = 'postgres'):
    '''
    Create an SQL Alchemy connection engine for the specified connection string credentials and return the engine.
    Current capability is limited to Postgres DBs. Base server is set for PG localhost inside a Docker container.
    '''    
    # Select engine connection string
    if db_type == 'postgres':
        conn_str =  URL.create(drivername="postgresql+psycopg2", username=user, password=pw, host=server, database=db, port=port, )
 
    if db_type == 'sqlserver':
        conn_str = URL.create(drivername="mssql+pyodbc", username=user, password=pw, host=server, database=db, port=port, 
                                query={"driver": "ODBC Driver 17 for SQL Server", "authentication": "ActiveDirectoryIntegrated"}, )

    # Create engine & execute query
    with create_engine(conn_str).connect() as cursor:
        raw = cursor.execute(text(query))
        
        # Extract table column names & row data 
        column_names = [col for col in raw.keys()]
        output = [row for row in raw]

    # Return as dictionary of lists e.g. JSON  
    return {col : [i[n] for i in output] for n, col in enumerate(column_names)}
