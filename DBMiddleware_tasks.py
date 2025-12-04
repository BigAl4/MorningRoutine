"""CRUD operations for the tasks table."""
from DBCommands import run_sql

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
    """Return all tasks ordered by FromTime."""
    return run_sql("SELECT id, FromTime, ToTime, TaskName, Active FROM tasks ORDER BY FromTime")

def toggle_task_active(task_id: int) -> int:
    """Invert the Active flag for a task. Returns rows affected (0 if id not found)."""
    row = get_task(task_id)
    if not row:
        return 0
    # row structure: (id, FromTime, ToTime, TaskName, Active)
    current_active = row[4]
    new_active = 0 if current_active else 1
    return update_task(task_id, active=bool(new_active))
