from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.forms import UserForm, ProfileForm
from accounts.models import Profile
from task_manager.models import Position

User = get_user_model()


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.login_url = reverse("accounts:login")
        self.task_url = reverse("task_manager:tasks")

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_valid_credentials(self):
        response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "testpassword"}
        )
        self.assertRedirects(response, self.task_url)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Invalid username or password"
            in response.context["form"].errors["__all__"]
        )
        self.assertTemplateUsed(response, "accounts/login.html")


class RegisterWorkerTests(TestCase):
    def setUp(self):
        self.register_url = reverse("accounts:register")
        self.task_url = reverse("task_manager:tasks")

    def test_register_worker_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_register_worker_post_valid(self):
        Position.objects.create(name="Developer")
        form_data = {
            "username": "newuser",
            "first_name": "First",
            "last_name": "Last",
            "email": "test@example.com",
            "position": Position.objects.first().id,
            "password1": "Complexpassword123",
            "password2": "Complexpassword123",
        }
        response = self.client.post(self.register_url, form_data)
        self.assertRedirects(response, self.task_url)
        self.assertEqual(User.objects.count(), 1)


class LogoutViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="testpassword")
        self.logout_url = reverse("accounts:logout")
        self.login_url = reverse("accounts:login")
        self.client.login(username="testuser", password="testpassword")

    def test_logout(self):
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)


class UserProfileUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )
        self.profile, created = Profile.objects.get_or_create(worker=self.user)
        self.url = reverse("accounts:profile_update")
        self.client.login(username="testuser", password="12345")

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            "accounts/user_profile_update_form.html"
        )

    def test_form_and_profile_form_in_context(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context["form"], UserForm)
        self.assertIsInstance(response.context["profile_form"], ProfileForm)
