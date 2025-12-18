import os
import sqlite3

from DBCommands import GetConn

# Create a cursor object
conn = GetConn()
cursor = conn.cursor()

# Create house_maintenance_tasks table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS house_maintenance_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL
    )
''')

cursor.execute('DELETE FROM house_maintenance_tasks')  # Clear existing data for idempotency
cursor.execute('''
    INSERT INTO house_maintenance_tasks (task_name) VALUES
    ('Yard Maintenance'),
    ('Organize a Drawer/Shelf'),
    ('Sell Unused Item on Marketplace'),
    ('Clean Eufy Vacuums'),
    ('Laundry'),
    ('Organize Computer Files'),
    ('Cleanup Office');
''')

# Create TASKS table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        FromTime TIME NOT NULL,
        ToTime TIME NOT NULL,
        TaskName TEXT NOT NULL,
        Active BOOLEAN NOT NULL DEFAULT 1
    )
''')

cursor.execute('DELETE FROM tasks')  # Clear existing data for idempotency
cursor.execute('''
    INSERT INTO tasks (FromTime, ToTime, TaskName, Active) VALUES
        ('07:30', '08:00', 'Wake Up & Stretch', 1),
        ('08:00', '08:30', 'Breakfast', 1),
        ('08:30', '09:30', 'Stock Research', 1),
        ('09:30', '10:00', 'House Maintenance Task', 1),
        ('10:00', '11:00', 'Focused Work Session', 1),
        ('11:00', '11:30', 'Break / Walk', 1),
        ('11:30', '12:00', 'Daily Goal Setting', 1),
        ('12:00', '12:30', 'Wrap Up Morning Routine', 1);
''')

# Create End of Day Notes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS end_of_day_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note TEXT NOT NULL,
        DateAdded DATE NOT NULL
    )
''')

cursor.execute('DELETE FROM end_of_day_notes')  # Clear existing data for idempotency

conn.commit()       # Commit the changes
conn.close()        # Close the connection

print("Database and tables created successfully.")
