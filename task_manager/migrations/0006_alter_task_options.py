# Generated by Django 5.0.6 on 2024-05-18 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0005_alter_task_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={"ordering": ["is_completed", "deadline"]},
        ),
    ]