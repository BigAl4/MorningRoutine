from DBMiddleware import (get_all_house_maint_tasks, get_house_maint_task_by_date, list_tasks,
                          add_note, get_note, update_note, delete_note, list_notes,
                          get_todays_note, get_yestedays_note)
from DBCommands import run_sql
from datetime import datetime, timedelta

# -----------------------------
# Helper functions
# -----------------------------
def add_note_for_yesterday(note: str) -> int:
    """Add a note for yesterday's date (skipping weekends).
    If today is Monday, adds note for Friday.
    If today is Sunday, adds note for Friday.
    Otherwise adds note for yesterday.
    Returns: new note id (int)
    """
    if not note or not note.strip():
        raise ValueError("Note cannot be blank.")
    
    today = datetime.now()
    weekday = today.weekday()  # Monday=0, Sunday=6
    
    if weekday == 0:  # Monday - add for Friday (3 days back)
        target_date = today - timedelta(days=3)
    elif weekday == 6:  # Sunday - add for Friday (2 days back)
        target_date = today - timedelta(days=2)
    else:  # Tuesday-Saturday - add for yesterday (1 day back)
        target_date = today - timedelta(days=1)
    
    target_date_str = target_date.strftime('%Y-%m-%d')
    sql = "INSERT INTO end_of_day_notes (note, DateAdded) VALUES (?, ?)"
    new_id = run_sql(sql, (note.strip(), target_date_str))
    return new_id

# -----------------------------
# Test cases
# -----------------------------
def test_select_all_house_maint_tasks():
    """Output all data from house_tasks table"""
    
    print("\n--- All Tasks from Database (SELECT * FROM house_tasks) ---")
    tasks = get_all_house_maint_tasks()
    for row in tasks:
        print(f"ID: {row[0]}, Task: {row[1]}")
    print(f"\nTotal tasks found: {len(tasks)}")

def test_select_all_tasks():
    """Output all data from tasks table."""
    
    print("\n--- All Tasks from Database (SELECT * FROM tasks) ---")
    tasks = list_tasks()
    if tasks:
        # Print field names for tasks table
        print("Fields: id, FromTime, ToTime, TaskName, Active")
        for row in tasks:
            print(row)
        print(f"\nTotal tasks found: {len(tasks)}")
    else:
        print("\nNo tasks found.")

def test_get_house_maint_task_by_date():
    print(get_house_maint_task_by_date('10/27/25') == "Yard Maintenance")
    print(get_house_maint_task_by_date('10/28/25') == "Organize a Drawer/Shelf")
    print(get_house_maint_task_by_date('10/29/25') == "Sell Unused Item on Marketplace")
    print(get_house_maint_task_by_date('10/30/25') == "Clean Eufy Vacuums")
    print(get_house_maint_task_by_date('10/31/25') == "Laundry")
    print(get_house_maint_task_by_date('11/01/25') == "Organize Computer Files")
    print(get_house_maint_task_by_date('11/02/25') == "Cleanup Office")
    print(get_house_maint_task_by_date('11/03/25') == "Yard Maintenance")  # Loop back

def test_end_of_day_notes():
    """Test End of Day Notes CRUD operations."""
    print("\n--- Testing End of Day Notes ---")
    
    # Test add_note
    print("\n1. Adding notes...")
    note_id_1 = add_note("Great progress on stock research today!")
    print(f"Added note id: {note_id_1}")
    note_id_2 = add_note("Completed house maintenance task successfully.")
    print(f"Added note id: {note_id_2}")
    
    # Test get_todays_note
    print("\n2. Getting today's notes...")
    todays_notes = get_todays_note()
    print(f"Today's notes count: {len(todays_notes)}")
    for note in todays_notes:
        print(f"  ID: {note[0]}, Note: {note[1]}, Date: {note[2]}")
    
    # Test get_note (single note)
    print("\n3. Getting single note...")
    note = get_note(note_id_1)
    if note:
        print(f"Retrieved note: {note}")
    else:
        print("Note not found")
    
    # Test update_note
    print("\n4. Updating note...")
    updated = update_note(note_id_1, "Updated: Had an excellent day with great progress!")
    print(f"Rows updated: {updated}")
    
    # Verify update
    updated_note = get_note(note_id_1)
    print(f"Updated note text: {updated_note[1]}")
    
    # Test list_notes (all notes)
    print("\n5. Listing all notes...")
    all_notes = list_notes()
    print(f"Total notes in database: {len(all_notes)}")
    
    # Test get_yestedays_note
    print("\n6. Getting yesterday's notes...")
    yesterdays_notes = get_yestedays_note()
    print(f"Yesterday's notes count: {len(yesterdays_notes)}")
    for note in yesterdays_notes:
        print(f"  ID: {note[0]}, Note: {note[1]}, Date: {note[2]}")
    
    # Test delete_note
    print("\n7. Deleting note...")
    deleted = delete_note(note_id_2)
    print(f"Rows deleted: {deleted}")
    
    # Verify deletion
    remaining_notes = get_todays_note()
    print(f"Remaining today's notes: {len(remaining_notes)}")


# -----------------------------
# Run tests
# -----------------------------
if __name__ == "__main__":
    test_select_all_tasks()
    test_select_all_house_maint_tasks()
    test_get_house_maint_task_by_date()
    test_end_of_day_notes()

