from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.models import Task, TaskType
from datetime import date


class ViewTestCase(TestCase):
    def setUp(self):
        # Создание пользователя
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client = Client()
        self.client.login(username="testuser", password="12345")

        # Создание типа задачи
        self.task_type = TaskType.objects.create(name="Bug")

        # Создание задачи
        self.task = Task.objects.create(
            name="Test Task",
            priority="High",
            task_type=self.task_type,
            is_completed=False,
            deadline=date.today(),
        )
        self.task.assignees.add(self.user)

    def test_index_view(self):
        response = self.client.get(reverse("task_manager:index"))
        self.assertEqual(response.status_code, 200)

    def test_tasks_view(self):
        response = self.client.get(reverse("task_manager:tasks"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_my_task_list_view(self):
        response = self.client.get(reverse("task_manager:my-task"))
        self.assertEqual(response.status_code, 200)

    def test_today_task_list_view(self):
        response = self.client.get(reverse("task_manager:today-task"))
        self.assertEqual(response.status_code, 200)

    def test_task_create_view(self):
        response = self.client.get(reverse("task_manager:create-task"))
        self.assertEqual(response.status_code, 200)

    def test_task_delete_view(self):
        response = self.client.get(
            reverse("task_manager:task-delete", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_task_update_view(self):
        response = self.client.get(
            reverse("task_manager:task-update", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_task_detail_view(self):
        response = self.client.get(
            reverse("task_manager:task-detail", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_task_dashboard_view(self):
        response = self.client.get(reverse("task_manager:task-dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_workers_list_view(self):
        response = self.client.get(reverse("task_manager:workers-list"))
        self.assertEqual(response.status_code, 200)

    def test_calendar_view(self):
        response = self.client.get(reverse("task_manager:calendar"))
        self.assertEqual(response.status_code, 200)

    def test_update_task_status(self):
        response = self.client.post(
            reverse("task_manager:task-complete"),
            {"task_id": self.task.id, "is_completed": "true"},
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
