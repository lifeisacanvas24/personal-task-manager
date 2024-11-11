# test_task_manager.py

import unittest

from modules.db_handler import (
    add_task,
    delete_task,
    fetch_task,
    init_db,
    list_tasks,
    update_task,
)


class TaskManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the database for testing
        init_db()

    def setUp(self):
        # Adding sample tasks for each test
        add_task("Sample Task", "A sample description", "Work", "Medium", "To Do", "2023-12-01", "14:00", 0)
        add_task("Urgent Task", "High priority task", "Personal", "High", "Doing", "2023-11-15", "09:00", 0)

    def tearDown(self):
        # Clean up tasks after each test to reset the environment
        tasks = list_tasks()
        for task in tasks:
            delete_task(task[0])

    def test_create_task(self):
        # Ensure that a new task is created
        add_task("New Test Task", "Test description", "Development", "Low", "To Do", "2023-12-31", "12:00", 0)
        tasks = list_tasks()
        self.assertTrue(any(task[1] == "New Test Task" for task in tasks), "Task creation failed")

    def test_update_task(self):
        # Ensure task is updated correctly
        task = list_tasks()[0]  # Get the first task
        update_task(task[0], {"title": "Updated Task Title"})
        updated_task = fetch_task(task[0])
        self.assertEqual(updated_task[1], "Updated Task Title", "Task update failed")

    def test_list_tasks_sorting(self):
        # Ensure that sorting by priority works
        tasks = list_tasks(sort_by="priority")
        self.assertEqual(tasks[0][4], "High", "Sorting by priority failed")

    def test_delete_task(self):
        # Test that a task is deleted correctly
        task_id = list_tasks()[0][0]  # Get the first task ID
        delete_task(task_id)
        deleted_task = fetch_task(task_id)
        self.assertIsNone(deleted_task, "Task deletion failed")

    def test_task_with_subtasks(self):
        # Create a task with subtasks and validate listing and deletion
        parent_task_id = list_tasks()[0][0]
        add_task("Subtask 1", "Subtask for testing", "Setup", "Medium", "To Do", "2023-12-20", "10:00", parent_task_id)

        tasks = list_tasks()
        subtask = next((task for task in tasks if task[8] == parent_task_id), None)
        self.assertIsNotNone(subtask, "Subtask creation failed")

        # Ensure deletion of parent task removes subtasks
        delete_task(parent_task_id)
        deleted_subtask = fetch_task(subtask[0])
        self.assertIsNone(deleted_subtask, "Subtask deletion failed when parent task deleted")

if __name__ == "__main__":
    unittest.main()
