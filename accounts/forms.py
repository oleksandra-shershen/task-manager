from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import Profile
from task_manager.models import Position, Worker

User = get_user_model()


class WorkerRegistrationForm(UserCreationForm):
    position = forms.ModelChoiceField(queryset=Position.objects.all())

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ['username', 'first_name', 'last_name', 'email', 'position']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'position']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'main_programming_language']
