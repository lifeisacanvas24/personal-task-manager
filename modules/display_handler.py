import textwrap

from tabulate import tabulate


# Function to display a list of tasks in tabular form with improved task hierarchy
def display_tasks(tasks, wrap_width=50):
    """Display tasks in a tabular form with wrapped descriptions for improved readability.

    :param tasks: List of task dictionaries
    :param wrap_width: The maximum width for wrapping text (default: 50 characters)
    """
    # Define headers for the table
    headers = ["ID", "Title", "Description", "Category", "Priority", "Status", "Due Date", "Time", "Parent ID"]

    # Prepare data for tabulate
    table_data = []
    for task in tasks:
        # Wrap the description to the specified width
        wrapped_description = "\n".join(textwrap.wrap(task['description'], wrap_width)) if task['description'] else "N/A"

        task_data = [
            task['id'],  # ID
            task['title'] if task['parent_id'] == 0 else f"  → {task['title']}",  # Indentation for subtasks
            wrapped_description,  # Wrapped Description
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
def display_task_details(task, wrap_width=50):
    """Display detailed information about a single task with wrapped fields.

    :param task: Task dictionary
    :param wrap_width: The maximum width for wrapping text (default: 50 characters)
    """
    print("Displaying task details")
    headers = ["Field", "Value"]

    # Wrap the description if it exceeds the wrap width
    wrapped_description = "\n".join(textwrap.wrap(task['description'], wrap_width)) if task['description'] else "N/A"

    task_details = [
        ["ID", task['id']],
        ["Title", task['title']],
        ["Description", wrapped_description],
        ["Category", task['category']],
        ["Priority", task['priority']],
        ["Status", task['status']],
        ["Due Date", task['due_date']],
        ["Time", task['time']],
        ["Parent ID", task['parent_id']]
    ]

    # Print task details in a table format
    print(tabulate(task_details, headers=headers, tablefmt="grid"))
