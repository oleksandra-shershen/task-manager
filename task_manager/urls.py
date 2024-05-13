from django.urls import path

from .views import index, tasks_view, MyTaskListView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", tasks_view, name="tasks"),
    path("tasks/my/", MyTaskListView.as_view(), name="my-task"),
]

app_name = "task_manager"
