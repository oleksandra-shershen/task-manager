from django.urls import path

from accounts.views import login_view, register_worker, logout_view, WorkerProfileDetailView, UserProfileView

urlpatterns = [
    path("login/", login_view, name="login"),
    path('register/', register_worker, name='register'),
    path('logout/', logout_view, name='logout'),
    path("user/profile/<int:pk>", WorkerProfileDetailView.as_view(), name="worker-profile-detail"),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
app_name = "accounts"
