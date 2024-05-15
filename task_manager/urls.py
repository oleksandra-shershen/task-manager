from django.urls import path

from .views import index, tasks_view, MyTaskListView, TodayTaskListView, TaskCreateView, TaskDeleteView, task_summary, calendar_view

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", tasks_view, name="tasks"),
    path("tasks/my/", MyTaskListView.as_view(), name="my-task"),
    path("tasks/today/", TodayTaskListView.as_view(), name="today-task"),
    path("tasks/create/", TaskCreateView.as_view(), name="create-task"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path('tasks/overview/', task_summary, name='overview'),
    path('tasks/calendar/', calendar_view, name='calendar'),

]

app_name = "task_manager"
