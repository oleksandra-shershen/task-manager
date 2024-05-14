from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from task_manager.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'priority', 'deadline', 'task_type', 'assignees']
        widgets = {
            'assignees': forms.CheckboxSelectMultiple(),
            'deadline': DatePickerInput(),
            "description": forms.widgets.Textarea(attrs={"rows": "3"}),
        }
