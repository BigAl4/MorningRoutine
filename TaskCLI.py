"""Interactive CLI for managing tasks in the MorningRoutine database. Run: python TaskCLI.py """

import re
from DBMiddleware import (list_tasks, add_task, update_task, delete_task, get_task, toggle_task_active,
                          get_all_house_maint_tasks, add_house_maint_task, update_house_maint_task,
                          delete_house_maint_task, get_house_maint_task,
                          add_note, get_note, update_note, delete_note, list_notes, 
                          list_notes_by_date, get_todays_note, get_yestedays_note)

MENU = """
--- Task Manager ---
1. Print Today's Plan
2. Edit Tasks Table
3. Edit House Maintenance Table
4. Edit End of Day Notes
5. Exit
Choose: """

EDITS_MENU = """
--- Tasks Table Edits ---
1. List tasks
2. Add task
3. Edit task
4. Delete task
5. Toggle active
6. Back to Main Menu
Choose: """

HOUSE_MAINT_MENU = """
--- House Maintenance Table Edits ---
1. List house maintenance tasks
2. Add house maintenance task
3. Edit house maintenance task
4. Delete house maintenance task
5. Back to Main Menu
Choose: """

NOTES_MENU = """
--- End of Day Notes ---
1. View today's notes
2. View all notes
3. Add note
4. Edit note
5. Delete note
6. Back to Main Menu
Choose: """

def is_valid_time(time_str):
    """Check if time is in HH:MM format (24-hour)."""
    return bool(re.match(r'^\d{2}:\d{2}$', time_str))

def display_tasks():
    rows = list_tasks()
    if not rows:
        print("No tasks found.")
        return
    print("\nID  From   To     Active Name")
    print("--  -----  -----  ------ ------------------------------")
    for r in rows:
        tid, fr, to, name, active = r
        print(f"{tid:<3} {fr:<5} {to:<5} {'Y' if active else 'N':<6} {name}")
    print()

def prompt_add():
    print("Add new task:")
    fr = input("From time (HH:MM): ").strip()
    to = input("To time (HH:MM): ").strip()
    name = input("Task name: ").strip()
    if not fr or not to or not name:
        print("Error: From time, To time, and Task name cannot be blank. Record not saved.")
        return
    if not is_valid_time(fr) or not is_valid_time(to):
        print("Error: Times must be in HH:MM format (e.g., 09:30). Record not saved.")
        return
    active_in = input("Active? (y/n) [y]: ").strip().lower() or 'y'
    active = active_in.startswith('y')
    new_id = add_task(fr, to, name, active)
    print(f"Inserted task id {new_id}.")

def prompt_edit():
    display_tasks()
    tid_str = input("Task id to edit: ").strip()
    if not tid_str.isdigit():
        print("Invalid id.")
        return
    tid = int(tid_str)
    row = get_task(tid)
    if not row:
        print("Task not found.")
        return
    _, fr_old, to_old, name_old, active_old = row
    print("Press Enter to keep existing value.")
    fr = input(f"From time [{fr_old}]: ").strip() or fr_old
    to = input(f"To time [{to_old}]: ").strip() or to_old
    name = input(f"Task name [{name_old}]: ").strip() or name_old
    if not fr or not to or not name:
        print("Error: From time, To time, and Task name cannot be blank. Record not saved.")
        return
    if not is_valid_time(fr) or not is_valid_time(to):
        print("Error: Times must be in HH:MM format (e.g., 09:30). Record not saved.")
        return
    active_in = input(f"Active (y/n) [{'y' if active_old else 'n'}]: ").strip().lower()
    active = active_old if active_in == '' else active_in.startswith('y')
    updated = update_task(tid, from_time=fr, to_time=to, task_name=name, active=active)
    print(f"Updated {updated} row(s).")

def prompt_delete():
    display_tasks()
    tid_str = input("Task id to delete: ").strip()
    if not tid_str.isdigit():
        print("Invalid id.")
        return
    tid = int(tid_str)
    confirm = input("Confirm delete? Type 'yes': ").strip().lower()
    if confirm != 'yes':
        print("Aborted.")
        return
    deleted = delete_task(tid)
    print(f"Deleted {deleted} row(s).")

def prompt_toggle():
    tid_str = input("Task id to toggle active: ").strip()
    if not tid_str.isdigit():
        print("Invalid id.")
        return
    tid = int(tid_str)
    affected = toggle_task_active(tid)
    if affected:
        print("Toggled active state.")
    else:
        print("Task not found.")

def print_todays_plan():
    """Print a concise ordered list of active tasks with time ranges."""
    rows = list_tasks()
    active_rows = [r for r in rows if r[4]]  # r = (id, FromTime, ToTime, TaskName, Active)
    if not active_rows:
        print("No active tasks for today.\n")
    else:
        print("\nToday's Plan:")
        print("Time Range   Task")
        print("-----------  ------------------------------")
        for _, fr, to, name, _ in active_rows:
            print(f"{fr}-{to:<9} {name}")
        print()
    
    # Print yesterday's end of day notes
    yesterday_notes = get_yestedays_note()
    if yesterday_notes:
        print("Yesterday's Reflection:")
        print("-" * 40)
        print(yesterday_notes[1])  # yesterday_notes[1] is the note text
        print()

def edits_submenu():
    """Handle the Tasks Table Edits submenu."""
    while True:
        choice = input(EDITS_MENU).strip()
        if choice == '1':
            display_tasks()
        elif choice == '2':
            prompt_add()
        elif choice == '3':
            prompt_edit()
        elif choice == '4':
            prompt_delete()
        elif choice == '5':
            prompt_toggle()
        elif choice == '6':
            break
        else:
            print("Invalid selection. Returning to main menu.")
            break

def display_house_maint_tasks():
    """Display all house maintenance tasks."""
    rows = get_all_house_maint_tasks()
    if not rows:
        print("No house maintenance tasks found.")
        return
    print("\nID  Task Name")
    print("--  ----------------------------------------")
    for r in rows:
        tid, name = r
        print(f"{tid:<3} {name}")
    print()

def prompt_add_house_maint():
    """Add a new house maintenance task."""
    print("Add new house maintenance task:")
    name = input("Task name: ").strip()
    if not name:
        print("Error: Task name cannot be blank. Record not saved.")
        return
    new_id = add_house_maint_task(name)
    print(f"Inserted house maintenance task id {new_id}.")

def prompt_edit_house_maint():
    """Edit an existing house maintenance task."""
    display_house_maint_tasks()
    tid_str = input("Task id to edit: ").strip()
    if not tid_str.isdigit():
        print("Invalid id.")
        return
    tid = int(tid_str)
    row = get_house_maint_task(tid)
    if not row:
        print("Task not found.")
        return
    _, name_old = row
    print(f"Current name: {name_old}")
    name = input("New task name (press Enter to keep): ").strip() or name_old
    if not name:
        print("Error: Task name cannot be blank. Record not saved.")
        return
    updated = update_house_maint_task(tid, name)
    print(f"Updated {updated} row(s).")

def prompt_delete_house_maint():
    """Delete a house maintenance task."""
    display_house_maint_tasks()
    tid_str = input("Task id to delete: ").strip()
    if not tid_str.isdigit():
        print("Invalid id.")
        return
    tid = int(tid_str)
    confirm = input("Confirm delete? Type 'yes': ").strip().lower()
    if confirm != 'yes':
        print("Aborted.")
        return
    deleted = delete_house_maint_task(tid)
    print(f"Deleted {deleted} row(s).")

def house_maint_submenu():
    """Handle the House Maintenance Table Edits submenu."""
    while True:
        choice = input(HOUSE_MAINT_MENU).strip()
        if choice == '1':
            display_house_maint_tasks()
        elif choice == '2':
            prompt_add_house_maint()
        elif choice == '3':
            prompt_edit_house_maint()
        elif choice == '4':
            prompt_delete_house_maint()
        elif choice == '5':
            break
        else:
            print("Invalid selection. Returning to main menu.")
            break

def display_notes(notes):
    """Display a list of notes."""
    if not notes:
        print("No notes found.")
        return
    print("\nID  Date       Note")
    print("--  ---------- " + "-" * 40)
    for r in notes:
        note_id, note, date_added = r
        note_preview = note[:40] + "..." if len(note) > 40 else note
        print(f"{note_id:<3} {date_added:<10} {note_preview}")
    print()

def prompt_add_note():
    """Add a new end of day note."""
    print("Add new end of day note:")
    note = input("Note (up to 255 characters): ").strip()
    if not note:
        print("Error: Note cannot be blank. Record not saved.")
        return
    try:
        new_id = add_note(note)
        print(f"Inserted note id {new_id}.")
    except ValueError as e:
        print(f"Error: {e}")

def prompt_edit_note():
    """Edit an existing note."""
    notes = get_todays_note()
    display_notes(notes)
    note_id_str = input("Note id to edit: ").strip()
    if not note_id_str.isdigit():
        print("Invalid id.")
        return
    note_id = int(note_id_str)
    row = get_note(note_id)
    if not row:
        print("Note not found.")
        return
    _, note_old, _ = row
    print(f"Current note: {note_old}")
    note = input("New note (press Enter to keep): ").strip() or note_old
    if not note:
        print("Error: Note cannot be blank. Record not saved.")
        return
    try:
        updated = update_note(note_id, note)
        print(f"Updated {updated} row(s).")
    except ValueError as e:
        print(f"Error: {e}")

def prompt_delete_note():
    """Delete a note."""
    notes = get_todays_note()
    display_notes(notes)
    note_id_str = input("Note id to delete: ").strip()
    if not note_id_str.isdigit():
        print("Invalid id.")
        return
    note_id = int(note_id_str)
    confirm = input("Confirm delete? Type 'yes': ").strip().lower()
    if confirm != 'yes':
        print("Aborted.")
        return
    deleted = delete_note(note_id)
    print(f"Deleted {deleted} row(s).")

def notes_submenu():
    """Handle the End of Day Notes submenu."""
    while True:
        choice = input(NOTES_MENU).strip()
        if choice == '1':
            notes = get_todays_note()
            display_notes(notes)
        elif choice == '2':
            notes = list_notes()
            display_notes(notes)
        elif choice == '3':
            prompt_add_note()
        elif choice == '4':
            prompt_edit_note()
        elif choice == '5':
            prompt_delete_note()
        elif choice == '6':
            break
        else:
            print("Invalid selection. Returning to main menu.")
            break


def main():
    while True:
        choice = input(MENU).strip()
        if choice == '':
            print("Goodbye.")
            break
        elif choice == '1':
            print_todays_plan()
        elif choice == '2':
            edits_submenu()
        elif choice == '3':
            house_maint_submenu()
        elif choice == '4':
            notes_submenu()
        elif choice == '5':
            print("Goodbye.")
            break
        else:
            print("Invalid selection.")

if __name__ == '__main__':
    main()
