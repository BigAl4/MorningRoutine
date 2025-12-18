MorningRoutine Project
======================

CHANGES:
    11/20/25  (Run TaskCLI.py to run the program now!!!)
        - Added menuing system to allow user to Add/Edit/Delete database entries in the TASKS table.
        - Added another menu option to Print Today's Plan
        - Updated the run_sql() command to return lastrowid (for inserts), rowcount (for updates/deletes), and results (for selects)
        - Changed all routines to use my run_sql() command to eliminate redundant connecting/executing/closing of database connection syntax.
        - Injected the House Maintenance Task (which changes day-to-day, and comes from its own table) into the results.
        - Adjusted the Edit/Delete tasks to LIST all of the tasks with their IDs so the user can choose which one to edit/delete.  Previously the
          program just asked for which ID to edit/delete.

  12/1/25
        - Add editing features for the add_house_maint_task table
        - Main menu is getting crowded, so add a sub-menu for table editing.
        - Fix bug whereby blank entries could be saved to the tables.
      
        - Optimizations made:
              1) Orgainze code in DBMiddleware.  Created a file for all editing code for each table.
              2) Validate formatting on inputted times.
              3) Numerous other optimizations were proposed, but I need more time to evaluate them.
      
       - CLEAR (Correct, Logical, Efficient, Appropriate, Readable) notes:
              1) Moving table-specific code was a logical recommendation.  Efficient for programmer, since not wading through code of a table that isn't applicable.
              2) Proposed change was tested and CORRECT, LOGICAL and APPROPRIATE, as previous version would save any values entered.
              3) I didn't fully understand the other numerous optimizations proposed, so chose not to include them yet.  Some were "ninja-code" and weren'table
                  obvious.  Caching was proposed, but given my experience can result in refreshing issues.  I need to understand their proposed code better
                  before accepting further proposed enhancements.

      12/28/25 (Late submission; This was due last week, but I was away for daughter's graduation and move)
       - Assignment 7 - Add New Feature/Secure Your code 
            1) Fixed bug
            2) Added EndOfDayNotes feature.  Allows ad-hoc notes to be added that will be shown the following
               (mainly needed to add stock symbols for options that didn't execute today, so I remember to follow-up on them the following day)
            3) Security Issues:
                  - Parameterized SQL queries are already done.
                  - Optionally recommended to encrypt the database, however I'm going to pass on this for now.
                  - CoPilot gave me a "perfectly adequate" security score based upon current codebase.

ToDo:
      Test cases were put in a Unittest framework for the factorial example.  Add them to this project

==================================================================================================================================================
SQLite-backed morning routine/task scheduler.

Database Setup
--------------
Run `python Setup.py` to (re)create and seed the `MorningRoutine.db` database.

Core Modules
------------
- `DBCommands.py`: Connection helper and generic SQL executor.
- `DBMiddleware.py`: Higher-level task access (listing, date-based selection) plus CRUD helpers.
- `TaskCLI.py`: Interactive command-line interface for managing tasks.

Tasks Table Schema
------------------
`tasks(id INTEGER PK, FromTime TIME, ToTime TIME, TaskName TEXT, Active BOOLEAN)`

CRUD Functions (DBMiddleware)
----------------------------
- `add_task(from_time, to_time, task_name, active=True) -> int`
- `update_task(task_id, from_time=None, to_time=None, task_name=None, active=None) -> int`
- `delete_task(task_id) -> int`
- `get_task(task_id) -> tuple | None`
- `list_tasks() -> list[tuple]` ordered by `FromTime`
- `toggle_task_active(task_id) -> int`

Using the CLI
-------------
1. Ensure DB is initialized: `python Setup.py`
2. Launch manager: `python TaskCLI.py`
3. Use menu options to list/add/edit/delete/toggle tasks.

Example Programmatic Usage
--------------------------
```
from DBMiddleware import add_task, list_tasks, update_task, delete_task
new_id = add_task('06:00', '06:30', 'Meditation', True)
print(list_tasks())
update_task(new_id, task_name='Morning Meditation')
delete_task(new_id)
```

Regenerating Database Safely
----------------------------
Re-running `Setup.py` clears and reseeds both tables; do not run if you want to keep custom entries.

Next Ideas
----------
- Add validation for time formats.
- Provide export/import (CSV/JSON).
- Optionally create a simple Flask web UI.

