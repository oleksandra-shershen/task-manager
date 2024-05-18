import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from task_manager.forms import TaskForm, TaskUpdateForm
from task_manager.models import Task, TaskType


@login_required
def index(request):
    return render(request, "task_manager/home_page.html")


@login_required
def tasks_view(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, "task_manager/index.html", context)


class MyTaskListView(LoginRequiredMixin, generic.ListView):
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
    model = Task
    template_name = "task_manager/today_task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TodayTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        today = datetime.date.today()

        today_tasks = Task.objects.filter(
            assignees=user,
            is_completed=False,
            deadline__year=today.year,
            deadline__month=today.month,
            deadline__day=today.day,
        ).select_related()

        context["today_tasks"] = today_tasks
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/task_form.html"
    success_url = reverse_lazy("task_manager:tasks")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/task_confirm_delete.html"
    success_url = reverse_lazy("task_manager:tasks")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(assignees=self.request.user)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "task_manager/task_update_form.html"
    success_url = reverse_lazy("task_manager:tasks")

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = 'task_manager/task_detail.html'
    context_object_name = 'task'


class TaskDashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "task_manager/task_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_columns = {}
        for task_type in TaskType.TASK_TYPE_CHOICES:
            task_columns[task_type[1]] = Task.objects.filter(
                task_type__name=task_type[0], is_completed=False
            )
        context["task_columns"] = task_columns
        return context


def task_summary(request):
    num_urgent_tasks = Task.objects.filter(priority="Urgent").count()
    num_low_tasks = Task.objects.filter(priority="Low").count()
    num_medium_tasks = Task.objects.filter(priority="Medium").count()
    num_high_tasks = Task.objects.filter(priority="High").count()

    return render(
        request,
        "task_manager/overview.html",
        {
            "num_urgent_tasks": num_urgent_tasks,
            "num_low_tasks": num_low_tasks,
            "num_medium_tasks": num_medium_tasks,
            "num_high_tasks": num_high_tasks,
        },
    )


def calendar_view(request):
    if request.user.is_authenticated:
        assigned_tasks = Task.objects.filter(
            assignees=request.user, deadline__isnull=False
        )
        tasks_for_calendar = [
            {
                "title": task.name.replace("'", "\\'").replace('"', '\\"'),
                "start": task.deadline.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            for task in assigned_tasks
        ]
    else:
        tasks_for_calendar = []
    context = {"tasks_for_calendar": tasks_for_calendar}
    return render(request, "task_manager/calendar_task.html", context)


@require_POST
@csrf_exempt
def update_task_status(request):
    task_id = request.POST.get("task_id")
    is_completed = request.POST.get("is_completed") == "true"
    task = Task.objects.get(id=task_id)
    task.is_completed = is_completed
    task.save()
    return JsonResponse({"status": "success"})
