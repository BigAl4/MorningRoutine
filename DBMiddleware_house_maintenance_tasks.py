"""CRUD operations for the house_maintenance_tasks table."""
from DBCommands import run_sql
from GenericFunctions import parse_date
from datetime import datetime

def get_all_house_maint_tasks():
    """Retrieve and display all tasks from the house_maintenance_tasks table using SELECT *.
    Returns:
    - List of tuples containing (id, task_name) for each row in the table."""

    # Execute SELECT * to get all columns from all rows
    tasks = run_sql("SELECT * FROM house_maintenance_tasks")
    return tasks

def get_house_maint_task_by_date(date_str: str) -> str:
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

def add_house_maint_task(task_name: str) -> int:
    """Insert a new task into the house_maintenance_tasks table.
    Returns: new task id (int)"""
    new_id = run_sql(
        "INSERT INTO house_maintenance_tasks (task_name) VALUES (?)",
        (task_name,)
    )
    return new_id

def update_house_maint_task(task_id: int, task_name: str) -> int:
    """Update a house maintenance task name. Returns rows affected."""
    count = run_sql(
        "UPDATE house_maintenance_tasks SET task_name = ? WHERE id = ?",
        (task_name, task_id)
    )
    return count

def delete_house_maint_task(task_id: int) -> int:
    """Delete a house maintenance task by id. Returns rows affected."""
    count = run_sql("DELETE FROM house_maintenance_tasks WHERE id = ?", (task_id,))
    return count

def get_house_maint_task(task_id: int):
    """Return a single house maintenance task row by id or None if not found."""
    results = run_sql("SELECT * FROM house_maintenance_tasks WHERE id = ?", (task_id,))
    return results[0] if results else None
