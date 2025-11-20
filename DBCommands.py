import os
import sqlite3
from GenericFunctions import parse_date

# Module-level constant for the database name
DB_NAME = 'MorningRoutine.db'

def GetConn():
    """Return a connection to the MorningRoutine.db database.
    
    Returns:
    - sqlite3.Connection: Active database connection object
    """
    dbPath = os.path.join(os.getcwd(), DB_NAME)
    conn = sqlite3.connect(dbPath)
    return conn

def run_sql(sql: str, params=None):
    """
    Connects to the SQLite database, executes the given SQL statement,
    and returns the results (if any).
    
    Parameters:
        sql (str): The SQL statement to execute.
        params (tuple or dict, optional): Parameters for parameterized queries.
    Returns:
        For SELECT: list of tuples (query results)
        For INSERT: lastrowid (int)
        For UPDATE/DELETE: rowcount (int) 
        On error: list with single tuple [("Error", error_message)]
    """
    conn = GetConn()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        # If it's a SELECT, fetch results
        if sql.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
        else:
            conn.commit()
            # Return lastrowid for INSERT, rowcount for UPDATE/DELETE
            if sql.strip().upper().startswith("INSERT"):
                results = cursor.lastrowid
            else:
                results = cursor.rowcount
    except sqlite3.Error as e:
        results = [("Error", str(e))]
    finally:
        conn.close()
    
    return results