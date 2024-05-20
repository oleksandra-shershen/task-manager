from django.core.exceptions import ValidationError
from django.test import TestCase

from task_manager.models import Position, Worker
from accounts.models import Profile
from phonenumber_field.phonenumber import PhoneNumber


class ProfileModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="john_doe",
            email="john.doe@example.com",
            password="12345",
            position=self.position,
        )
        Profile.objects.filter(worker=self.worker).delete()

    def test_profile_creation(self):
        profile = Profile.objects.create(
            worker=self.worker,
            phone=PhoneNumber.from_string(
                phone_number="+1234567890",
                region="US"
            ),
            main_programming_language="Python",
        )
        self.assertEqual(profile.worker, self.worker)
        self.assertEqual(str(profile.phone), "+1234567890")
        self.assertEqual(profile.main_programming_language, "Python")

    def test_profile_on_worker_delete(self):
        self.worker.delete()
        self.assertEqual(Profile.objects.count(), 0)

    def test_profile_str_representation(self):
        profile = Profile.objects.create(
            worker=self.worker, main_programming_language="Python"
        )
        expected_representation = (
            f"{self.worker.username} ({self.worker.get_full_name()}) - Python"
        )
        self.assertEqual(str(profile), expected_representation)

    def test_profile_phone_validation(self):
        profile = Profile(
            worker=self.worker,
            phone="12345",
            main_programming_language="Python",
        )
        with self.assertRaises(ValidationError):
            profile.full_clean()
