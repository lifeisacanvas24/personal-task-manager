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
# Add a new task to the database
def add_task(title, description, category, priority, status, due_date, time, parent_id=0, recurrence="none", dependencies="[]"):
    try:
        conn = sqlite3.connect('db/tasks.db')
        cursor = conn.cursor()

        # Calculate the initial next occurrence based on recurrence interval
        next_occurrence = None
        if recurrence != "none" and due_date:
            current_date = datetime.strptime(due_date, "%Y-%m-%d")
            next_occurrence = calculate_next_occurrence(recurrence, current_date)

        # Insert the task into the database
        cursor.execute('''INSERT INTO tasks (title, description, category, priority, status, due_date, time, parent_id, recurrence, next_occurrence, dependencies)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (title, description, category, priority, status, due_date, time, parent_id, recurrence, next_occurrence, dependencies))
        conn.commit()

        # Fetch and return the last inserted task ID
        task_id = cursor.lastrowid
        return task_id
    except sqlite3.Error as e:
        print(f"Error adding task: {e}")
        logging.error("Error adding task: %s", e)
        return None
    finally:
        conn.close()

# Fetch a task by ID
def fetch_task(task_id):
    conn = sqlite3.connect('db/tasks.db')
    cursor = conn.cursor()

    # Fetch the task as a tuple
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task_tuple = cursor.fetchone()
    conn.close()

    if task_tuple:
        # Convert the tuple to a dictionary for easier access
        columns = ["id", "title", "description", "category", "priority", "status", "due_date", "time", "parent_id", "recurrence", "next_occurrence", "dependencies"]
        task = dict(zip(columns, task_tuple))
        return task
    return None

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
# List tasks with optional filtering and sorting
def list_tasks(filters=None, sort_by=None):
    """Fetch tasks from the database with optional filters and sorting.

    :param filters: A dictionary of filters (e.g., {"parent_id": 2, "status": "To Do"})
    :param sort_by: A comma-separated string of fields to sort by (e.g., "due-date,priority")
    :return: A list of tasks matching the criteria
    """
    try:
        conn = sqlite3.connect('db/tasks.db')
        cursor = conn.cursor()

        # Base query
        query = "SELECT * FROM tasks"
        conditions = []
        values = []

        # Apply filters
        if filters:
            if "task_title" in filters:
                conditions.append("title LIKE ?")
                values.append(filters["task_title"].replace("*", "%"))  # Support wildcards
            if "parent_id" in filters:
                conditions.append("parent_id = ?")
                values.append(filters["parent_id"])
            if "status" in filters:
                conditions.append("status = ?")
                values.append(filters["status"])
            if "priority" in filters:
                conditions.append("priority = ?")
                values.append(filters["priority"])
            if "category" in filters:
                conditions.append("category = ?")
                values.append(filters["category"])

        # Add conditions to query
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Apply sorting
        if sort_by:
            sort_fields = ", ".join(sort_by.split(","))
            query += f" ORDER BY {sort_fields}"

        # Execute the query
        cursor.execute(query, tuple(values))
        tasks = cursor.fetchall()

        # Convert tuples to dictionaries
        task_list = []
        for task in tasks:
            task_dict = {
                "id": task[0],
                "title": task[1],
                "description": task[2],
                "category": task[3],
                "priority": task[4],
                "status": task[5],
                "due_date": task[6],
                "time": task[7],
                "parent_id": task[8],
                "recurrence": task[9],
                "next_occurrence": task[10],
                "dependencies": task[11]
            }
            task_list.append(task_dict)

        return task_list

    except sqlite3.Error as e:
        print(f"Error listing tasks: {e}")
        return []
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
