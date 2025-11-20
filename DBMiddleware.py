import os, sqlite3
from DBCommands import GetConn, run_sql
from datetime import datetime
from GenericFunctions import parse_date

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

def add_task(from_time: str, to_time: str, task_name: str, active: bool = True) -> int:
    """Insert a new task into the tasks table.
    Inputs:
    - from_time: start time in HH:MM (24h) format
    - to_time: end time in HH:MM (24h) format
    - task_name: descriptive name for the task
    - active: whether the task is active (default True)
    Returns: new task id (int)
    """
    new_id = run_sql(
        "INSERT INTO tasks (FromTime, ToTime, TaskName, Active) VALUES (?, ?, ?, ?)",
        (from_time, to_time, task_name, 1 if active else 0)
    )
    return new_id

def update_task(task_id: int, from_time: str | None = None, to_time: str | None = None,
                task_name: str | None = None, active: bool | None = None) -> int:
    """Update fields of an existing task by id.
    Only provided (non-None) parameters are updated.
    Returns: number of rows affected (0 if id not found)."""
    fields = []
    values = []
    if from_time is not None:
        fields.append("FromTime = ?")
        values.append(from_time)
    if to_time is not None:
        fields.append("ToTime = ?")
        values.append(to_time)
    if task_name is not None:
        fields.append("TaskName = ?")
        values.append(task_name)
    if active is not None:
        fields.append("Active = ?")
        values.append(1 if active else 0)
    if not fields:
        raise ValueError("No fields provided to update.")
    sql = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
    values.append(task_id)
    count = run_sql(sql, tuple(values))
    return count

def delete_task(task_id: int) -> int:
    """Delete a task by id. Returns number of rows deleted (0 if none)."""
    count = run_sql("DELETE FROM tasks WHERE id = ?", (task_id,))
    return count

def get_task(task_id: int):
    """Return a single task row (tuple) by id or None if not found."""
    results = run_sql("SELECT * FROM tasks WHERE id = ?", (task_id,))
    return results[0] if results else None

def list_tasks():
    """Return all tasks ordered by FromTime, with today's house maintenance task injected."""
    tasks = run_sql("SELECT id, FromTime, ToTime, TaskName, Active FROM tasks ORDER BY FromTime")
    
    # Get today's date in MM/DD/YY format
    today = datetime.now().strftime('%m/%d/%y')
    house_task = get_house_maint_task_by_date(today)
    
    # Find and update the "House Maintenance Task" entry
    updated_tasks = []
    for task in tasks:
        tid, fr, to, name, active = task
        if "House Maintenance Task" in name:
            # Replace with today's specific house maintenance task
            updated_tasks.append((tid, fr, to, house_task, active))
        else:
            updated_tasks.append(task)
    
    return updated_tasks

def toggle_task_active(task_id: int) -> int:
    """Invert the Active flag for a task. Returns rows affected (0 if id not found)."""
    row = get_task(task_id)
    if not row:
        return 0
    # row structure: (id, FromTime, ToTime, TaskName, Active)
    current_active = row[4]
    new_active = 0 if current_active else 1
    return update_task(task_id, active=bool(new_active))

