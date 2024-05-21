# Generated by Django 4.2.13 on 2024-05-21 13:28

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="Mobile phone number",
                        max_length=128,
                        null=True,
                        region=None,
                    ),
                ),
                (
                    "main_programming_language",
                    models.CharField(default="Not specified.", max_length=255),
                ),
            ],
        ),
    ]
