from django.http import HttpResponse
from django.shortcuts import render

from task_manager.models import Task


def index(request):
    """View function for the home page of the site."""
    return render(request, "task_manager/home_page.html")


def tasks_view(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, "task_manager/index.html", context)
