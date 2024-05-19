from django.urls import path

from accounts.views import login_view, register_worker, logout_view, WorkerProfileDetailView

urlpatterns = [
    path("login/", login_view, name="login"),
    path('register/', register_worker, name='register'),
    path('logout/', logout_view, name='logout'),
    path("user/profile/<int:pk>", WorkerProfileDetailView.as_view(), name="worker-profile-detail"),
]
app_name = "accounts"
