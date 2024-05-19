from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from accounts.forms import WorkerRegistrationForm, LoginForm
from task_manager.models import Worker


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("task_manager:tasks"))
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {'form': form})


def register_worker(request):
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_manager:tasks')
    else:
        form = WorkerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    """
    Logs out the current user and redirects to the login page.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('accounts:login')


class WorkerProfileDetailView(LoginRequiredMixin, generic.DetailView):
    """DetailView class for user profile page."""

    model = Worker
    template_name = "accounts/worker_profile_detail.html"