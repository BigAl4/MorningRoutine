import os
import sqlite3
from GenericFunctions import parse_date

# Module-level constant for the database name
DB_NAME = 'MorningRoutine.db'

def GetConn():
    """Return a connection to the ProgrammingWithAI.db database.
    
    Returns:
    - sqlite3.Connection: Active database connection object
    """
    dbPath = os.path.join(os.getcwd(), DB_NAME)
    conn = sqlite3.connect(dbPath)
    return conn

def run_sql(sql: str):
    """
    Connects to the SQLite database, executes the given SQL statement,
    and returns the results (if any).
    
    Parameters:
        sql (str): The SQL statement to execute.
    Returns:
        list: Query results as a list of tuples, or an empty list if no results.
    """
    conn = GetConn()
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql)
        # If it's a SELECT, fetch results
        if sql.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
        else:
            conn.commit()
            results = []
    except sqlite3.Error as e:
        results = [("Error", str(e))]
    finally:
        conn.close()
    
    return results