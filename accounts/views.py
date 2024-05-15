from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import WorkerRegistrationForm


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "accounts/login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("task_manager:tasks"))
        else:
            error_context = {
                "error": "Invalid credentials"
            }
            return render(
                request,
                "accounts/login.html",
                context=error_context
            )


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