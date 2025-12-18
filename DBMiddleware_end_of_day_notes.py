"""CRUD operations for the End of Day Notes table."""
from DBCommands import run_sql
from datetime import datetime, timedelta

def add_note(note: str) -> int:
    """Insert a new end of day note.
    Inputs:
    - note: note text (supports at least 50 characters)
    Returns: new note id (int)
    """
    if not note or not note.strip():
        raise ValueError("Note cannot be blank.")
    today = datetime.now().strftime('%Y-%m-%d')
    sql = "INSERT INTO end_of_day_notes (note, DateAdded) VALUES (?, ?)"
    new_id = run_sql(sql, (note.strip(), today))
    return new_id

def get_note(note_id: int):
    """Return a single note row by id or None if not found."""
    sql = "SELECT * FROM end_of_day_notes WHERE id = ?"
    results = run_sql(sql, (note_id,))
    return results[0] if results else None

def update_note(note_id: int, note: str) -> int:
    """Update a note's text. Returns rows affected (0 if id not found)."""
    if not note or not note.strip():
        raise ValueError("Note cannot be blank.")
    sql = "UPDATE end_of_day_notes SET note = ? WHERE id = ?"
    count = run_sql(sql, (note.strip(), note_id))
    return count

def delete_note(note_id: int) -> int:
    """Delete a note by id. Returns rows affected (0 if id not found)."""
    sql = "DELETE FROM end_of_day_notes WHERE id = ?"
    count = run_sql(sql, (note_id,))
    return count

def list_notes():
    """Return all notes ordered by DateAdded (newest first)."""
    sql = "SELECT id, note, DateAdded FROM end_of_day_notes ORDER BY DateAdded DESC, id DESC"
    return run_sql(sql)

def list_notes_by_date(date_str: str):
    """Return all notes for a specific date (YYYY-MM-DD format)."""
    sql = "SELECT id, note, DateAdded FROM end_of_day_notes WHERE DateAdded = ? ORDER BY id DESC"
    return run_sql(sql, (date_str,))

def get_todays_note():
    """Return all notes for today."""
    today = datetime.now().strftime('%Y-%m-%d')
    return list_notes_by_date(today)

def get_yestedays_note():
    """Return all notes for yesterday, skipping weekends.
    If today is Monday, returns Friday's notes.
    If today is Sunday, returns Friday's notes.
    Otherwise returns yesterday's notes.
    """
    today = datetime.now()
    weekday = today.weekday()  # Monday=0, Sunday=6
    
    if weekday == 0:  # Monday - get Friday (3 days back)
        target_date = today - timedelta(days=3)
    elif weekday == 6:  # Sunday - get Friday (2 days back)
        target_date = today - timedelta(days=2)
    else:  # Tuesday-Saturday - get yesterday (1 day back)
        target_date = today - timedelta(days=1)
    
    target_date_str = target_date.strftime('%Y-%m-%d')
    return list_notes_by_date(target_date_str)
