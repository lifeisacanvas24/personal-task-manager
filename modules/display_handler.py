from tabulate import tabulate


# Function to display a list of tasks in tabular form with improved task hierarchy
# Function to display a list of tasks in tabular form with improved task hierarchy
def display_tasks(tasks):
    # Define headers for the table
    headers = ["ID", "Title", "Description", "Category", "Priority", "Status", "Due Date", "Time", "Parent ID"]

    # Prepare data for tabulate
    table_data = []
    for task in tasks:
        task_data = [
            task['id'],  # ID
            task['title'] if task['parent_id'] == 0 else f"  → {task['title']}",  # Indentation for subtasks
            task['description'] if task['description'] else "N/A",  # Handle empty description
            task['category'],  # Category
            task['priority'],  # Priority
            task['status'],  # Status
            task['due_date'] if task['due_date'] else "N/A",  # Handle empty due date
            task['time'] if task['time'] else "N/A",  # Handle empty time
            task['parent_id']   # Parent ID
        ]
        table_data.append(task_data)

    # Print the formatted table with grid
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Function to display individual task details
def display_task_details(task):
    print("Displaying task details")
    headers = ["Field", "Value"]
    task_details = [
        ["ID", task['id']],
        ["Title", task['title']],
        ["Description", task['description']],
        ["Category", task['category']],
        ["Priority", task['priority']],
        ["Status", task['status']],
        ["Due Date", task['due_date']],
        ["Time", task['time']],
        ["Parent ID", task['parent_id']]
    ]

    # Print task details in a table format
    print(tabulate(task_details, headers=headers, tablefmt="grid"))
