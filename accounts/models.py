from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from task_manager.models import Worker


class Profile(models.Model):
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE)

    phone = PhoneNumberField(blank=True, null=True, help_text="Mobile phone number")
    main_programming_language = models.CharField(max_length=255, default="")

    def save(self, *args, **kwargs):
        super().save()
