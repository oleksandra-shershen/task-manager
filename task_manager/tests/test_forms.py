from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.test import TestCase
from task_manager.forms import TaskForm, TaskUpdateForm
from task_manager.models import Task, TaskType
from django.contrib.auth import get_user_model


class TaskFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Old Task",
            description="Old description",
            priority="High",
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user)

    def test_task_form_init_without_instance(self):
        form = TaskForm()
        self.assertIsNone(
            form.instance.pk
        )

    def test_task_form_init_with_instance(self):
        form = TaskForm(instance=self.task)
        self.assertEqual(
            form.instance.pk, self.task.pk
        )

    def test_task_form_valid_data(self):
        form = TaskForm(
            data={
                "name": "New Task",
                "description": "New description",
                "priority": "Medium",
                "task_type": self.task_type.pk,
                "assignees": [self.user.pk],
            },
            instance=self.task,
        )
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_data(self):
        form = TaskForm(
            data={
                "name": "",
                "description": "New description",
                "priority": "Medium",
                "task_type": self.task_type.pk,
                "assignees": [self.user.pk],
            }
        )
        self.assertFalse(form.is_valid())

    def test_task_update_form_widgets(self):
        form = TaskUpdateForm()
        self.assertIsInstance(form.fields["deadline"].widget, DatePickerInput)
        self.assertIsInstance(form.fields["description"].widget, forms.Textarea)
        self.assertIsInstance(
            form.fields["assignees"].widget, forms.CheckboxSelectMultiple
        )
