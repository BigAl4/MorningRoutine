import os, sqlite3
from DBCommands import GetConn, run_sql
from datetime import datetime
from GenericFunctions import parse_date

def get_all_tasks():
    """Retrieve and display all tasks from the tasks table using SELECT *.
    Returns:
    - List of tuples containing (id, task_name) for each row in the table."""

    # Execute SELECT * to get all columns from all rows
    tasks = run_sql("SELECT * FROM tasks")
    return tasks

def get_all_house_maint_tasks():
    """Retrieve and display all tasks from the house_maintenance_tasks table using SELECT *.
    Returns:
    - List of tuples containing (id, task_name) for each row in the table."""

    # Execute SELECT * to get all columns from all rows
    tasks = run_sql("SELECT * FROM house_maintenance_tasks")
    return tasks

def get_task_by_date(date_str: str) -> str:
    """Return the task name for a given date by cycling through tasks.
    Inputs:
    - date_str: a date string in MM/DD/YY format.
    Behavior:
    - Reads all task names from the SQLite DB table `house_maintenance_tasks`.
    - Uses the date's ordinal number to compute an index into the task list, cycling with modulo.
    Returns:
    - The selected task name, or a fallback message if no tasks exist.
    """
    # Convert string to date
    date = parse_date(date_str)
    
    # Connect to the SQLite database located in the current project directory.
    # Note: `Setup.py` initializes and populates this database.
    results = run_sql("SELECT task_name FROM house_maintenance_tasks ORDER BY id") # Get all tasks ordered by their id for deterministic cycling
    tasks = [row[0] for row in results]

    if not tasks:
        return "No tasks available."

    day_number = date.toordinal()       # Convert date to ordinal number for consistent indexing (1..N)
    index = (day_number - 1) % len(tasks)       # Use modulo to cycle through tasks across days
    return tasks[index]

