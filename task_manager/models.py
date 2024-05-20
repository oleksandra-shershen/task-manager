from django.contrib.auth.models import AbstractUser
from django.db import models

from task_manager_service import settings


class Position(models.Model):
    POSITION_CHOICES = (
        ("Developer", "Developer"),
        ("Project Manager", "Project Manager"),
        ("Designer", "Designer"),
        ("DevOps", "DevOps"),
        ("QA", "QA"),
    )

    name = models.CharField(max_length=255, choices=POSITION_CHOICES)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TaskType(models.Model):
    TASK_TYPE_CHOICES = (
        ("Bug", "Bug"),
        ("New Feature", "New Feature"),
        ("Refactoring", "Refactoring"),
        ("QA", "QA"),
    )

    name = models.CharField(
        max_length=255, choices=TASK_TYPE_CHOICES, blank=True, null=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        related_name="workers",
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("Urgent", "Urgent"),
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    created_date = models.DateField(auto_now_add=True, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    is_completed = models.BooleanField(default=False)
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="assigned_tasks"
    )

    class Meta:
        ordering = ["is_completed", "deadline"]

    def __str__(self):
        return self.name
