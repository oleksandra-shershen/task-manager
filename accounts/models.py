from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from task_manager.models import Worker


class Profile(models.Model):
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE)

    phone = PhoneNumberField(
        blank=True,
        null=True,
        help_text="Mobile phone number"
    )
    main_programming_language = models.CharField(
        max_length=255,
        default="Not specified."
    )

    def __str__(self):
        full_name = self.worker.get_full_name()
        return (f"{self.worker.username} "
                f"({full_name}) - {self.main_programming_language}")

    def save(self, *args, **kwargs):
        super().save()
