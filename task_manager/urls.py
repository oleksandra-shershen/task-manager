from django.urls import path

from task_manager.views import (
    index,
    tasks_view,
    MyTaskListView,
    TodayTaskListView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    TaskDashboardView,
    calendar_view,
    update_task_status,
    TaskDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", tasks_view, name="tasks"),
    path("tasks/my/", MyTaskListView.as_view(), name="my-task"),
    path("tasks/today/", TodayTaskListView.as_view(), name="today-task"),
    path("tasks/create/", TaskCreateView.as_view(), name="create-task"),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/calendar/", calendar_view, name="calendar"),
    path(
        "tasks/dashboard/",
        TaskDashboardView.as_view(),
        name="task-dashboard"
    ),
    path(
        "tasks/update-task-status/",
        update_task_status,
        name="task-complete"
    ),
]

app_name = "task_manager"
