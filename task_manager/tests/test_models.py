from django.test import TestCase
from task_manager.models import Position, TaskType, Task
from django.contrib.auth import get_user_model


class PositionModelTest(TestCase):
    def test_string_representation(self):
        position = Position(name="Developer")
        self.assertEqual(str(position), "Developer")


class TaskTypeModelTest(TestCase):
    def test_string_representation(self):
        task_type = TaskType(name="Bug")
        self.assertEqual(str(task_type), "Bug")


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = get_user_model().objects.create_user(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="12345",
        )
        self.user.position = self.position
        self.user.save()

    def test_string_representation(self):
        self.assertEqual(str(self.user), "john_doe (John Doe)")


class TaskModelTest(TestCase):
    def setUp(self):
        task_type = TaskType.objects.create(name="Bug")
        user = get_user_model().objects.create_user(
            "jane_doe", "jane.doe@example.com", "12345"
        )
        self.task = Task.objects.create(
            name="Fix login bug",
            description="Fixes the bug in the login page",
            priority="Urgent",
            task_type=task_type,
        )
        self.task.assignees.add(user)

    def test_string_representation(self):
        self.assertEqual(str(self.task), "Fix login bug")

    def test_task_fields(self):
        self.assertEqual(self.task.name, "Fix login bug")
        self.assertEqual(self.task.description, "Fixes the bug in the login page")
        self.assertEqual(self.task.priority, "Urgent")
        self.assertTrue(self.task.assignees.exists())
