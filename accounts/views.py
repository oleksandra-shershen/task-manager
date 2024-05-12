from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, 'accounts/login.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("task_manager:task-list"))
        else:
            error_context = {
                "error": "Invalid credentials"
            }
            return render(request, 'accounts/login.html', context=error_context)
