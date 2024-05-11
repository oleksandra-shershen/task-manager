from django.db import models

from task_manager.models import Worker


class Profile(models.Model):
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save()
