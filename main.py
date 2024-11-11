import logging
import traceback

from modules.cli_handler import parse_arguments
from modules.db_handler import (
    add_task,
    delete_task,
    fetch_task,
    init_db,
    list_tasks,
    update_task,
)
from modules.display_handler import display_task_details, display_tasks

# Configure logging
logging.basicConfig(filename='task_manager.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Initialize database
    init_db()

    # Parse arguments
    args = parse_arguments()

    try:
        if args.command == "create":
            # Log task creation attempt
            logging.info("Attempting to create task with title: %s", args.task_title)
            add_task(
                title=args.task_title,
                description=args.description,
                category=args.category,
                priority=args.priority,
                status=args.status,
                due_date=args.due_date,
                time=args.time,
                parent_id=args.parent_id
            )
            logging.info("Task created successfully with title: %s", args.task_title)
            print("Task created successfully!")

        elif args.command == "update":
            task = fetch_task(args.task_id)
            if task is None:
                logging.warning("Update failed. Task with ID %s not found", args.task_id)
                print("Task not found.")
                return

            # Log update attempt and display current task details
            logging.info("Attempting to update task ID %s", args.task_id)

            # Convert task tuple to dictionary for easier manipulation
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
                "dependencies": task[11],
            }

            print("Current Task Details:")
            display_task_details(task_dict)

            updates = {}
            if args.task_title and args.task_title != task_dict["title"]: updates["title"] = args.task_title
            if args.description and args.description != task_dict["description"]: updates["description"] = args.description
            if args.category and args.category != task_dict["category"]: updates["category"] = args.category
            if args.priority and args.priority != task_dict["priority"]: updates["priority"] = args.priority
            if args.status and args.status != task_dict["status"]: updates["status"] = args.status
            if args.due_date and args.due_date != task_dict["due_date"]: updates["due_date"] = args.due_date
            if args.time and args.time != task_dict["time"]: updates["time"] = args.time
            if args.parent_id is not None and args.parent_id != task_dict["parent_id"]: updates["parent_id"] = args.parent_id

            # Add this check to handle if there are no updates
            if not updates:
                logging.warning("No updates provided for task ID %s", args.task_id)
                print("No changes were made to the task.")
                return

            # Log the updates before executing SQL
            print(f"Executing SQL: UPDATE tasks SET {', '.join([f'{key} = ?' for key in updates])} WHERE id = ? with values {tuple(updates.values())}")

            # Confirm update
            confirm = input("\nDo you want to update this task? (y/n): ").strip().lower()
            if confirm == 'y':
                update_task(args.task_id, updates)
                logging.info("Task ID %s updated successfully", args.task_id)
                print("Task updated successfully!")
            else:
                logging.info("Task update canceled for ID %s", args.task_id)
                print("Task update canceled.")

        elif args.command == "list":
            tasks = list_tasks(sort_by=args.sort_by if args.all else None)
            display_tasks(tasks)
            logging.info("Listed tasks with sort option: %s", args.sort_by)

        elif args.command == "delete":
            task = fetch_task(args.task_id)
            if task is None:
                logging.warning("Delete failed. Task with ID %s not found", args.task_id)
                print("Task not found.")
                return

            print("Task to be deleted:")
            display_task_details(task)

            subtasks = [t for t in list_tasks() if t[8] == args.task_id]
            if subtasks:
                print("\nThis task has the following subtasks:")
                display_tasks(subtasks)

            confirm = input("Do you want to delete this task and its subtasks? (y/n): ").strip().lower()
            if confirm == 'y':
                delete_task(args.task_id)
                logging.info("Task ID %s and subtasks deleted successfully", args.task_id)
                print("Task and subtasks deleted successfully!")
            else:
                logging.info("Task deletion canceled for ID %s", args.task_id)
                print("Task deletion canceled.")

        else:
            logging.error("Invalid command received: %s", args.command)
            print("Invalid command. Use --help for usage information.")

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        logging.error("Traceback: %s", traceback.format_exc())
        print("An error occurred. Check the log for details.")

if __name__ == "__main__":
    main()
