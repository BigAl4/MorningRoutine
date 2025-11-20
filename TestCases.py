from DBMiddleware import get_all_house_maint_tasks, get_house_maint_task_by_date, get_all_tasks  # Import from module without .py suffix

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
    tasks = get_all_tasks()
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

# -----------------------------
# Run tests
# -----------------------------
if __name__ == "__main__":
    test_select_all_tasks()
    test_select_all_house_maint_tasks()
    test_get_house_maint_task_by_date()
