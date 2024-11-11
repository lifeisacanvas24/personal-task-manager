# modules/cli_handler.py

import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Personal Task Manager")

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Task management commands")

    # Create command with recurrence and dependencies
    create_parser = subparsers.add_parser("create", help="Create a new task")
    create_parser.add_argument("-tt", "--task-title", required=True, help="Title of the task")
    create_parser.add_argument("-td", "--description", help="Description of the task")
    create_parser.add_argument("-c", "--category", choices=['Work', 'Personal', 'Careers Related', 'Home', 'Development', 'Research', 'Setup', 'Configuration'], required=True, help="Category of the task")
    create_parser.add_argument("-p", "--priority", choices=['High', 'Medium', 'Low'], required=True, help="Priority level")
    create_parser.add_argument("-s", "--status", choices=['To Do', 'Doing', 'Done'], required=True, help="Task status")
    create_parser.add_argument("-dd", "--due-date", help="Due date for the task (e.g., YYYY-MM-DD)")
    create_parser.add_argument("-ti", "--time", help="Time for the task (e.g., HH:MM)")
    create_parser.add_argument("-pid", "--parent-id", type=int, default=0, help="Parent ID if this is a subtask (default is 0)")
    create_parser.add_argument("-rec", "--recurrence", choices=["none", "daily", "weekly", "monthly"], default="none", help="Set recurrence for task")
    create_parser.add_argument("-dep", "--dependencies", help="Comma-separated list of task IDs this task depends on")


    # --- Update command ---
    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("-tid", "--task-id", type=int, required=True, help="ID of the task to update")
    update_parser.add_argument("-tt", "--task-title", help="New title of the task")
    update_parser.add_argument("-td", "--description", help="New description of the task")
    update_parser.add_argument("-c", "--category", choices=['Work', 'Personal', 'Careers Related', 'Home', 'Development', 'Research', 'Setup', 'Configuration'], help="New category of the task")
    update_parser.add_argument("-p", "--priority", choices=['High', 'Medium', 'Low'], help="New priority level")
    update_parser.add_argument("-s", "--status", choices=['To Do', 'Doing', 'Done'], help="New status")
    update_parser.add_argument("-dd", "--due-date", help="New due date for the task (e.g., YYYY-MM-DD)")
    update_parser.add_argument("-ti", "--time", help="New time for the task (e.g., HH:MM)")
    update_parser.add_argument("-pid", "--parent-id", type=int, help="New parent ID if this is a subtask")

    # --- List command ---
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("-a", "--all", action="store_true", help="List all tasks")
    list_parser.add_argument("-sb", "--sort-by", choices=["due-date", "priority", "category", "task-id", "status"], help="Sort tasks by specified field")

    # --- Delete command ---
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("-tid", "--task-id", type=int, required=True, help="ID of the task to delete")

    return parser.parse_args()
