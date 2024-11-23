import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Personal Task Manager: Manage your tasks effectively with advanced filtering, sorting, recurrence, and dependencies.",
        epilog="""
Examples of Usage:
  1. Create a new task with recurrence and dependencies:
     py main.py create -tt "Submit Resume" -td "Submit CV to Germany Agencies" -c "Careers Related" -p "High" -s "To Do" -dd "2024-11-19" -rec "weekly" -dep "3,4"

  2. Update an existing task:
     py main.py update -tid 1 -tt "Updated Task Title" -s "Doing"

  3. List tasks with multiple filters and sorting:
     py main.py list --task-title "*Recruitment*" --parent-id 2 --status "To Do" --sort-by "priority,due-date"

  4. Delete a task along with its subtasks:
     py main.py delete -tid 5
"""
    )

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Task management commands")

    # --- Create command ---
    create_parser = subparsers.add_parser(
        "create",
        help="Create a new task. Supports recurrence and dependencies for advanced task management."
    )
    create_parser.add_argument("-tt", "--task-title", required=True, help="Title of the task (e.g., 'Submit Resume')")
    create_parser.add_argument("-td", "--description", help="Description of the task (e.g., 'Send CV to agencies')")
    create_parser.add_argument("-c", "--category", choices=[
        'Work', 'Personal', 'Careers Related', 'Home', 'Development', 'Research', 'Setup', 'Configuration'
    ], required=True, help="Category of the task (e.g., 'Careers Related')")
    create_parser.add_argument("-p", "--priority", choices=['High', 'Medium', 'Low'], required=True, help="Priority level")
    create_parser.add_argument("-s", "--status", choices=['To Do', 'Doing', 'Done'], required=True, help="Task status")
    create_parser.add_argument("-dd", "--due-date", help="Due date for the task in YYYY-MM-DD format (e.g., '2024-11-19')")
    create_parser.add_argument("-ti", "--time", help="Time for the task in HH:MM format (e.g., '14:00')")
    create_parser.add_argument("-pid", "--parent-id", type=int, default=0, help="Parent ID if this is a subtask (default is 0)")
    create_parser.add_argument("-rec", "--recurrence", choices=["none", "daily", "weekly", "monthly"], default="none", help="Set recurrence for the task")
    create_parser.add_argument("-dep", "--dependencies", help="Comma-separated list of task IDs this task depends on (e.g., '3,4')")

    # --- Update command ---
    update_parser = subparsers.add_parser(
        "update",
        help="Update an existing task. Provide only the fields to be updated."
    )
    update_parser.add_argument("-tid", "--task-id", type=int, required=True, help="ID of the task to update")
    update_parser.add_argument("-tt", "--task-title", help="New title of the task")
    update_parser.add_argument("-td", "--description", help="New description of the task")
    update_parser.add_argument("-c", "--category", choices=[
        'Work', 'Personal', 'Careers Related', 'Home', 'Development', 'Research', 'Setup', 'Configuration'
    ], help="New category of the task")
    update_parser.add_argument("-p", "--priority", choices=['High', 'Medium', 'Low'], help="New priority level")
    update_parser.add_argument("-s", "--status", choices=['To Do', 'Doing', 'Done'], help="New status")
    update_parser.add_argument("-dd", "--due-date", help="New due date for the task in YYYY-MM-DD format")
    update_parser.add_argument("-ti", "--time", help="New time for the task in HH:MM format")
    update_parser.add_argument("-pid", "--parent-id", type=int, help="New parent ID if this is a subtask")

    # --- List command ---
    list_parser = subparsers.add_parser(
        "list",
        help="List all tasks with advanced filtering and sorting options."
    )
    list_parser.add_argument("-a", "--all", action="store_true", help="List all tasks")
    list_parser.add_argument("-tt", "--task-title", help="Filter by task title (supports wildcard '*')")
    list_parser.add_argument("-pid", "--parent-id", type=int, help="Filter by parent ID")
    list_parser.add_argument("-s", "--status", choices=["To Do", "Doing", "Done"], help="Filter by status")
    list_parser.add_argument("-p", "--priority", choices=["High", "Medium", "Low"], help="Filter by priority")
    list_parser.add_argument("-c", "--category", choices=[
        "Work", "Personal", "Careers Related", "Home", "Development", "Research", "Setup", "Configuration"
    ], help="Filter by category")
    list_parser.add_argument("-sb", "--sort-by", help="Comma-separated fields to sort by (e.g., 'due-date,priority')")

    # --- Delete command ---
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a task along with its subtasks. Asks for confirmation before deletion."
    )
    delete_parser.add_argument("-tid", "--task-id", type=int, required=True, help="ID of the task to delete")

    return parser.parse_args()
