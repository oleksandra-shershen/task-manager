from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import WorkerRegistrationForm, LoginForm


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
