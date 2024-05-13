from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from task_manager.models import Task


@login_required
def index(request):
    return render(request, "task_manager/home_page.html")


@login_required
def tasks_view(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, "task_manager/index.html", context)
