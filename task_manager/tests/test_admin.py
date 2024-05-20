from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.models import Position, TaskType, Worker, Task


class AdminTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="password123"
        )
        self.client = Client()
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="Developer")
        self.task_type = TaskType.objects.create(name="Bug")
        self.worker = Worker.objects.create_user(
            username="worker1", password="password123", position=self.position
        )
        self.task = Task.objects.create(
            name="Example Task", priority="High", task_type=self.task_type
        )
        self.task.assignees.add(self.worker)

    def test_admin_task_list_display(self):
        url = reverse("admin:task_manager_task_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Example Task")
        self.assertContains(response, "High")

    def test_admin_worker_list_display(self):
        url = reverse("admin:task_manager_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, "worker1")
        self.assertContains(response, "Developer")  # Позиция работника

    def test_admin_position_list_display(self):
        url = reverse("admin:task_manager_position_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Developer")

    def test_admin_tasktype_list_display(self):
        url = reverse("admin:task_manager_tasktype_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Bug")
