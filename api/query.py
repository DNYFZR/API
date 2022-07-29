# Generate query
def generate_query(
    table:str, select_col:str, 
    date_col:str, date_from:str, date_to:str, 
    tournament_col:str, tournament:str, 
    player_col:str, player:str
    ) -> str:
    
    ### Build base query string ###
    query = f'''SELECT * FROM {table} ;'''
    
    # Replace * with provided column names
    if select_col != None:
        if len(select_col) == 1:
            query = query.replace('*', select_col[0])
        else:
            query = query.replace('*', ', '.join(select_col).lstrip(', '))

    ### CTE's ###

    # CTE_0 : Date fiter (currently by year)
    if date_col != None and (date_from != None or date_to != None):     
        
        # All years up to date_to (inclusive)
        if date_to == None:
            cte = f'''WITH temp_table as 
                        (SELECT * FROM {table} WHERE EXTRACT(YEAR from {date_col}::DATE) >= {date_from})'''
        # All years from date_from (inclusive) 
        elif date_from == None:
            cte = f'''WITH temp_table as 
                        (SELECT * FROM {table} WHERE EXTRACT(YEAR from {date_col}::DATE) <= {date_to})'''
        # All years between date_from & date_to (inclusive)
        else:
            cte = f'''WITH temp_table as 
                        (SELECT * FROM {table} WHERE EXTRACT(YEAR from {date_col}::DATE) >= {date_from} AND EXTRACT(YEAR from {date_col}::DATE) <= {date_to} )'''

        query = f'''{cte} {query.replace(table, 'temp_table')}'''

    # CTE_1 : Tournament filter 
    if tournament_col != None and tournament != None:
        tournament = f''' '{tournament.replace('_', ' ').title()}' '''

        # Where there is no active CTE_0
        if date_col == None:
            cte = f'''WITH temp_table as (SELECT * FROM {table} WHERE {tournament_col} = {tournament})'''
            query = f'''{cte} {query.replace(table, 'temp_table')}'''
        # Where CTE_0 is active
        else:
            cte_1 = f''', temp_table_2 as (SELECT * FROM temp_table WHERE {tournament_col} = {tournament})'''
            cte_0, query = query.rsplit('SELECT', maxsplit=1)
            query = f'''{cte_0} {cte_1} SELECT {query.replace('temp_table', 'temp_table_2')}'''

    # CTE_2 : Player filter - allows multiple columns to be used (winner or loser etc.)
    if player_col != None and player != None:
        player = f''' '{player.replace('_', ' ').title()}' '''

        # If no other CTE's are active
        if date_col == None and tournament_col == None:
            # set base CTE with first column provided in WHERE clause
            cte = f'''WITH temp_table as (SELECT * FROM {table} WHERE {player_col[0]} = {player})'''

            # if there are more columns : add them to the string as OR statements within the WHERE clause
            if len(player_col) > 1:
                for column in player_col[1:]:
                    cte = cte.replace(')', f''' OR {column} = {player})''')
            
            # Combine the CTE with the main query
            query = f'''{cte} {query.replace(table, 'temp_table')}'''
        
        # If 1 other CTE is active
        elif (date_col != None and tournament_col == None) or (date_col == None and tournament_col != None): 
            # set base CTE with first column provided in WHERE clause
            cte_1 = f''', temp_table_2 as (SELECT * FROM temp_table WHERE {player_col[0]} = {player})'''
            
            # if there are more columns : add them to the string as OR statements within the WHERE clause
            if len(player_col) > 1:
                for column in player_col[1:]:
                    cte_1 = cte_1.replace(')', f''' OR {column} = {player})''')
            
            # Combine the CTE with the main query - split on the last SELECT statement to add in the new CTE in sequence
            cte_0, query = query.rsplit('SELECT', maxsplit=1)
            query = f'''{cte_0} {cte_1} SELECT {query.replace('temp_table', 'temp_table_2')}'''
     
        # If 2 other CTE's are active
        elif date_col != None and tournament_col != None: 
            # set base CTE with first column provided in WHERE clause
            cte_2 = f''', temp_table_3 as (SELECT * FROM temp_table_2 WHERE {player_col[0]} = {player})'''
            
            # if there are more columns : add them to the string as OR statements within the WHERE clause
            if len(player_col) > 1:
                for column in player_col[1:]:
                    cte_2 = cte_2.replace(')', f''' OR {column} = {player})''')

            # Combine the CTE with the main query - split on the last SELECT statement to add in the new CTE in sequence
            cte_0_1, query = query.rsplit('SELECT', maxsplit=1)
            query = f'''{cte_0_1} {cte_2} SELECT {query.replace('temp_table_2', 'temp_table_3')}'''

    return query

