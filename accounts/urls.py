from django.urls import path

from accounts.views import login_view, register_worker

urlpatterns = [
    path("login/", login_view, name="login"),
    path('register/', register_worker, name='register'),
]
app_name = "accounts"
