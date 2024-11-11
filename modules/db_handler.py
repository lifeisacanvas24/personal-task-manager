import json
import sqlite3
from datetime import datetime, timedelta


# Function to calculate the next occurrence date
def calculate_next_occurrence(recurrence, current_date):
    if recurrence == "daily":
        return (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
    if recurrence == "weekly":
        return (current_date + timedelta(weeks=1)).strftime("%Y-%m-%d")
    if recurrence == "monthly":
        # Add one month by manipulating the month field
        new_month = current_date.month % 12 + 1
        year_increment = (current_date.month + 1) // 12
        return current_date.replace(month=new_month, year=current_date.year + year_increment).strftime("%Y-%m-%d")
    return None

# Initialize database and create table
def init_db():
    try:
        conn = sqlite3.connect('db/tasks.db')
        cursor = conn.cursor()
        # Create tasks table with added columns for recurrence, next_occurrence, and dependencies
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               title TEXT NOT NULL,
                               description TEXT,
                               category TEXT CHECK(category IN ('Work', 'Personal', 'Careers Related', 'Home', 'Development', 'Research', 'Setup', 'Configuration')),
                               priority TEXT CHECK(priority IN ('High', 'Medium', 'Low')),
                               status TEXT CHECK(status IN ('To Do', 'Doing', 'Done')),
                               due_date TEXT,
                               time TEXT,
                               parent_id INTEGER DEFAULT 0,
                               recurrence TEXT DEFAULT 'none' CHECK(recurrence IN ('none', 'daily', 'weekly', 'monthly')),
                               next_occurrence TEXT,
                               dependencies TEXT DEFAULT '[]'
                             )''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

# Add a new task to the database
def add_task(title, description, category, priority, status, due_date, time, parent_id=0, recurrence="none", dependencies="[]"):
    conn = sqlite3.connect('db/tasks.db')
    cursor = conn.cursor()

    # Calculate the initial next occurrence based on recurrence interval
    next_occurrence = None
    if recurrence != "none" and due_date:
        current_date = datetime.strptime(due_date, "%Y-%m-%d")
        next_occurrence = calculate_next_occurrence(recurrence, current_date)

    cursor.execute('''INSERT INTO tasks (title, description, category, priority, status, due_date, time, parent_id, recurrence, next_occurrence, dependencies)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (title, description, category, priority, status, due_date, time, parent_id, recurrence, next_occurrence, dependencies))
    conn.commit()
    conn.close()

# Fetch a task by ID
def fetch_task(task_id):
    try:
        conn = sqlite3.connect('db/tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error fetching task: {e}")
        task = None
    finally:
        conn.close()
    return task

# Update task details
def update_task(task_id: int, updates: dict) -> None:
    try:
        conn = sqlite3.connect('db/tasks.db')
        cursor = conn.cursor()

        # Ensure updates is a dictionary and log the content
        print(f"Updates: {updates}, Type of updates: {type(updates)}")

        # Generate columns with placeholders
        columns = ', '.join(f"{k} = ?" for k in updates)
        values = list(updates.values())  # Get the values to update
        values.append(task_id)  # Append task_id at the end for WHERE clause

        # Debugging line: print the SQL being executed
        print(f"Executing SQL: UPDATE tasks SET {columns} WHERE id = ? with values {tuple(values)}")

        # Execute the update query
        result = cursor.execute(f'UPDATE tasks SET {columns} WHERE id = ?', tuple(values))
        conn.commit()

        # Log the number of rows affected
        rows_affected = result.rowcount
        print(f"Rows affected: {rows_affected}")

        if rows_affected == 0:
            print("No rows were updated. It might be because the task's current values match the proposed updates.")

    except sqlite3.Error as e:
        print(f"Error updating task: {e}")
    finally:
        conn.close()

# Delete task by ID
def delete_task(task_id):
    try:
        conn = sqlite3.connect('db/tasks.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting task: {e}")
    finally:
        conn.close()

# List tasks with optional sorting
def list_tasks(sort_by=None):
    try:
        conn = sqlite3.connect('db/tasks.db')
        cursor = conn.cursor()

        query = "SELECT * FROM tasks"
        if sort_by:
            query += f" ORDER BY {sort_by}"

        cursor.execute(query)
        tasks = cursor.fetchall()

        # Convert tuples to dictionaries
        task_list = []
        for task in tasks:
            task_dict = {
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'category': task[3],
                'priority': task[4],
                'status': task[5],
                'due_date': task[6],
                'time': task[7],
                'parent_id': task[8],
                'recurrence': task[9],
                'next_occurrence': task[10],
                'dependencies': task[11]
            }
            task_list.append(task_dict)

        return task_list
    except sqlite3.Error as e:
        print(f"Error listing tasks: {e}")
    finally:
        conn.close()

# Validate task dependencies
def validate_dependencies(task_id):
    task = fetch_task(task_id)
    dependencies = json.loads(task[11])  # dependencies column
    for dep_id in dependencies:
        dep_task = fetch_task(dep_id)
        if dep_task is None or dep_task[5] != "Done":  # Status column
            return False
    return True

def mark_task_as_done_with_dependencies(task_id):
    if validate_dependencies(task_id):
        mark_task_as_done(task_id)
    else:
        print("Cannot mark this task as done. One or more dependencies are incomplete.")
