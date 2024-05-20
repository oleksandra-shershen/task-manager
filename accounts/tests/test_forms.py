from django.test import TestCase
from django.contrib.auth import get_user_model
from task_manager.models import Position
from accounts.forms import (
    WorkerRegistrationForm,
    LoginForm,
    UserForm,
    ProfileForm
)

User = get_user_model()


class WorkerRegistrationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")

    def test_form_save(self):
        form_data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "position": self.position.id,
            "password1": "complexpassword123",
            "password2": "complexpassword123",
        }
        form = WorkerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.position, self.position)


class LoginFormTest(TestCase):
    def test_form_fields(self):
        form = LoginForm()
        self.assertIn("username", form.fields)
        self.assertIn("password", form.fields)

    def test_form_validation(self):
        form_data = {"username": "user", "password": "pass"}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())


class UserFormTest(TestCase):
    def test_meta_model(self):
        form = UserForm()
        self.assertEqual(form._meta.model, User)
        self.assertEqual(
            form._meta.fields,
            ["first_name", "last_name", "email", "username", "position"],
        )


class ProfileFormTest(TestCase):
    def test_profile_form_fields(self):
        form = ProfileForm()
        self.assertIn("phone", form.fields)
        self.assertIn("main_programming_language", form.fields)

    def test_profile_form_save(self):
        form_data = {
            "phone": "+12125552368",
            "main_programming_language": "Python",
        }
        form = ProfileForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        profile = form.save(commit=False)
        self.assertEqual(profile.phone.as_e164, "+12125552368")
        self.assertEqual(profile.main_programming_language, "Python")
