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

            # Add task and capture the created task ID
            task_id = add_task(
                title=args.task_title,
                description=args.description,
                category=args.category,
                priority=args.priority,
                status=args.status,
                due_date=args.due_date,
                time=args.time,
                parent_id=args.parent_id,
                recurrence=args.recurrence,
                dependencies=args.dependencies or "[]"
            )

            if task_id:
                logging.info("Task created successfully with title: %s, ID: %s, Parent ID: %s", args.task_title, task_id, args.parent_id)
                print(f"Task created successfully! Task ID: {task_id}, Parent ID: {args.parent_id}")
            else:
                logging.error("Task creation failed for title: %s", args.task_title)
                print("Task creation failed. Check logs for details.")

        elif args.command == "update":
            # Fetch the task to update
            task = fetch_task(args.task_id)
            if task is None:
                logging.warning("Update failed. Task with ID %s not found", args.task_id)
                print(f"Task not found for ID {args.task_id}.")
                return

            # Display current task details
            logging.info("Attempting to update task ID %s", args.task_id)
            print("Current Task Details:")
            display_task_details(task)

            # Prepare updates based on arguments
            updates = {}
            if args.task_title:
                updates["title"] = args.task_title
            if args.description:
                updates["description"] = args.description
            if args.category:
                updates["category"] = args.category
            if args.priority:
                updates["priority"] = args.priority
            if args.status:
                updates["status"] = args.status
            if args.due_date:
                updates["due_date"] = args.due_date
            if args.time:
                updates["time"] = args.time
            if args.parent_id is not None:
                updates["parent_id"] = args.parent_id

            # Check if there are updates
            if not updates:
                logging.warning("No updates provided for task ID %s", args.task_id)
                print(f"No changes were made to the task ID {args.task_id}.")
                return

            # Confirm update
            print("\nUpdated Task Details (Proposed):")
            display_task_details({**task, **updates})
            confirm = input("Do you want to update this task? (y/n): ").strip().lower()
            if confirm == 'y':
                update_task(args.task_id, updates)
                logging.info("Task ID %s updated successfully", args.task_id)
                print(f"Task ID {args.task_id} updated successfully!")
            else:
                logging.info("Task update canceled for ID %s", args.task_id)
                print(f"Task update canceled for ID {args.task_id}.")

        elif args.command == "list":
            # Prepare filters and sorting
            filters = {}
            if args.task_title:
                filters["task_title"] = args.task_title
            if args.parent_id is not None:
                filters["parent_id"] = args.parent_id
            if args.status:
                filters["status"] = args.status
            if args.priority:
                filters["priority"] = args.priority
            if args.category:
                filters["category"] = args.category

            # Fetch tasks with filters and sorting
            tasks = list_tasks(filters=filters, sort_by=args.sort_by)
            if tasks:
                display_tasks(tasks)
            else:
                print("No tasks found matching the criteria.")
            logging.info("Listed tasks with filters: %s and sort option: %s", filters, args.sort_by)

        elif args.command == "delete":
            try:
                # Ensure the task ID is an integer
                task_id_int = int(args.task_id)
            except ValueError:
                logging.error("Invalid task ID: '%s'. Must be an integer.", args.task_id)
                print("Invalid task ID. Please provide an integer.")
                return

            # Fetch the task to confirm deletion
            task = fetch_task(task_id_int)
            if task is None:
                logging.warning("Task not found for ID %s", task_id_int)
                print(f"Task not found for ID {task_id_int}.")
                return

            # Display task details
            print("Task to be deleted:")
            display_task_details(task)

            # Fetch and display subtasks, if any
            subtasks = [t for t in list_tasks() if t["parent_id"] == task_id_int]
            if subtasks:
                print("\nThis task has the following subtasks:")
                display_tasks(subtasks)

            # Confirm deletion
            confirm = input("Do you want to delete this task and its subtasks? (y/n): ").strip().lower()
            if confirm == 'y':
                # Delete the main task and its subtasks
                delete_task(task_id_int)
                for subtask in subtasks:
                    delete_task(subtask["id"])  # Delete each subtask
                logging.info("Task ID %s and its subtasks deleted successfully.", task_id_int)
                print(f"Task ID {task_id_int} and its subtasks deleted successfully!")
            else:
                logging.info("Task deletion canceled for ID %s.", task_id_int)
                print(f"Task deletion canceled for ID {task_id_int}.")

        else:
            logging.error("Invalid command received: %s", args.command)
            print("Invalid command. Use --help for usage information.")

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        logging.error("Traceback: %s", traceback.format_exc())
        print("An error occurred. Check the log for details.")


if __name__ == "__main__":
    main()
