from django.urls import path

from accounts.views import login_view, register_worker, logout_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path('register/', register_worker, name='register'),
    path('logout/', logout_view, name='logout')
]
app_name = "accounts"
