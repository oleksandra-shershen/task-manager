import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import TaskForm, TaskUpdateForm
from task_manager.models import Task


@login_required
def index(request):
    """
    Renders the home page template for the task manager application.

    This view requires users to be logged in using the `@login_required` decorator.
    """
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_visits": num_visits + 1,
    }

    return render(request, "task_manager/home_page.html", context=context)


@login_required
def tasks_view(request):
    """
    Displays a list of all tasks in the system.

    This view retrieves all tasks from the Task model and renders them in the
    "task_manager/index.html" template.

    This view requires users to be logged in using the `@login_required` decorator.
    """
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, "task_manager/index.html", context)


class MyTaskListView(LoginRequiredMixin, generic.ListView):
    """
    ListView class that displays tasks assigned to the currently logged-in user.

    This view retrieves tasks from the Task model and filters them based on the following criteria:

    * **User:** Only tasks where the current user is included in the `assignees` field are displayed.
    * **Completion Status:** Only uncompleted tasks (where `is_completed` is False) are included.
    * **Search (Optional):** If a search parameter (`name`) exists in the GET request, the tasks are further
    filtered based on the name (using case-insensitive filtering).

    The view provides the following context variables to the template:

    * `my_tasks`: A list of filtered tasks assigned to the logged-in user.
    * `today_date`: The current date as a datetime.date object.

    This view requires users to be logged in using the `LoginRequiredMixin`.
    """

    model = Task
    template_name = "task_manager/my_task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        my_tasks = Task.objects.filter(
            assignees=user, is_completed=False
        ).select_related()

        if self.request.GET.get("name") is not None:
            my_tasks = my_tasks.filter(
                name__icontains=self.request.GET["name"], is_completed=False
            )

        context["my_tasks"] = my_tasks
        context["today_date"] = datetime.date.today()

        return context


class TodayTaskListView(LoginRequiredMixin, generic.ListView):
    """
    ListView class that displays tasks with deadlines set for today.

    This view retrieves tasks from the Task model and filters them based on the following criteria:

    * **User:** Only tasks where the current user is included in the `assignees` field are displayed.
    * **Completion Status:** Only uncompleted tasks (where `is_completed` is False) are included.
    * **Deadline:** Only tasks with deadlines set for the current date are included.

    The view provides the following context variable to the template:

    * `today_tasks`: A list of filtered tasks with deadlines set for today.

    This view requires users to be logged in using the `LoginRequiredMixin`.
    """

    model = Task
    template_name = "task_manager/today_task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TodayTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        today = datetime.date.today()

        today_tasks = Task.objects.filter(
            assignees=user, is_completed=False, deadline__year=today.year,
            deadline__month=today.month, deadline__day=today.day
        ).select_related()

        context["today_tasks"] = today_tasks
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_manager/task_form.html'
    success_url = reverse_lazy('task_manager:tasks')


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    # TO DO
    # Подумать над тем как обрабатывать кейсы(визуально), когда я
    # хочу удалить не свою таску
    model = Task
    template_name = 'task_manager/task_confirm_delete.html'
    success_url = reverse_lazy('task_manager:tasks')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(assignees=self.request.user)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'task_manager/task_update_form.html'
    success_url = reverse_lazy("task_manager:tasks")

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)


def task_summary(request):
    num_urgent_tasks = Task.objects.filter(priority='Urgent').count()
    num_low_tasks = Task.objects.filter(priority='Low').count()
    num_medium_tasks = Task.objects.filter(priority='Medium').count()
    num_high_tasks = Task.objects.filter(priority='High').count()

    return render(request, 'task_manager/overview.html', {
        'num_urgent_tasks': num_urgent_tasks,
        'num_low_tasks': num_low_tasks,
        'num_medium_tasks': num_medium_tasks,
        'num_high_tasks': num_high_tasks,
    })


def calendar_view(request):
    if request.user.is_authenticated:
        assigned_tasks = Task.objects.filter(assignees=request.user, deadline__isnull=False)
        tasks_for_calendar = [
            {
                'title': task.name.replace("'", "\\'").replace('"', '\\"'),  # Экранируем кавычки
                'start': task.deadline.strftime('%Y-%m-%dT%H:%M:%S'),
            }
            for task in assigned_tasks
        ]
    else:
        tasks_for_calendar = []
    context = {'tasks_for_calendar': tasks_for_calendar}
    return render(request, 'task_manager/calendar_task.html', context)


def kanban_board(request):
    context = {
        'to_do': Task.objects.filter(progress='To Do'),
        'in_progress': Task.objects.filter(progress='In Progress'),
        'in_review': Task.objects.filter(progress='In Review'),
        'testing': Task.objects.filter(progress='Testing'),
        'done': Task.objects.filter(progress='Done'),
    }
    return render(request, 'task_manager/kanban_board.html', context)
