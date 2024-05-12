from django.urls import path

from .views import index, tasks_view

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", tasks_view, name="task-list")
]

app_name = "task_manager"
