"""DBMiddleware - Re-exports CRUD functions from table-specific modules."""
from datetime import datetime
from DBMiddleware_tasks import (add_task, update_task, delete_task, get_task, 
                                list_tasks, toggle_task_active)
from DBMiddleware_house_maintenance_tasks import (get_all_house_maint_tasks, 
                                                  get_house_maint_task_by_date,
                                                  add_house_maint_task, 
                                                  update_house_maint_task,
                                                  delete_house_maint_task, 
                                                  get_house_maint_task)

def list_tasks_with_today_house_maint():
    """Return all tasks ordered by FromTime, with today's house maintenance task injected."""
    tasks = list_tasks()
    
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

# Override list_tasks to include today's house maintenance task
_original_list_tasks = list_tasks

def list_tasks():
    """Return all tasks ordered by FromTime, with today's house maintenance task injected."""
    tasks = _original_list_tasks()
    
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


