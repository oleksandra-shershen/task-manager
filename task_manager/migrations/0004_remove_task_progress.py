# Generated by Django 5.0.6 on 2024-05-18 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0003_task_progress"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="progress",
        ),
    ]
