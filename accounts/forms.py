from django.contrib.auth.forms import UserCreationForm
from django import forms

from task_manager.models import Position, Worker


class WorkerRegistrationForm(UserCreationForm):
    position = forms.ModelChoiceField(queryset=Position.objects.all())

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ['username', 'first_name', 'last_name', 'email', 'position']
