import secrets
import string
from typing import Any

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Schedule
from .serializers import ScheduleSerializer


# Helper function to generate a random password
def generate_random_password(length: int = 12) -> str:
    """Generate a random password."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


# Helper function to create test credentials
def create_test_user(username: str, password: str | None = None) -> User:
    """Create a test user with a random or given password."""
    if password is None:
        password = generate_random_password()  # Generate random password if none provided
    return User.objects.create_user(username=username, password=password)


# Helper function to create JWT tokens
def get_tokens_for_user(user: User) -> dict[str, Any]:
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class ScheduleAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user with a generated password
        self.password = generate_random_password()  # Random password for user
        self.user = create_test_user(username="testuser", password=self.password)
        tokens = get_tokens_for_user(self.user)
        self.access_token = tokens["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        # Create another user for ownership tests
        self.other_user = create_test_user(username="otheruser", password=generate_random_password())

        self.valid_schedule_data = {
            "schedule": {
                "monday": [
                    {"start": "08:00", "stop": "10:00", "ids": [1, 2]},
                    {"start": "11:00", "stop": "12:00", "ids": [3, 4]},
                ],
                "tuesday": [{"start": "08:00", "stop": "17:00", "ids": [5, 6]}],
            }
        }

        self.invalid_schedule_data = {"schedule": {"monday": [{"stop": "10:00", "ids": [1, 2]}]}}

        self.invalid_day_schedule_data = {"schedule": {"funday": [{"start": "08:00", "stop": "10:00", "ids": [1, 2]}]}}

        self.missing_ids_schedule_data = {"schedule": {"monday": [{"start": "08:00", "stop": "10:00"}]}}

    # Authentication Tests
    def test_signup_success(self):
        self.client.credentials()  # No auth token required for signup
        signup_data = {"username": "newuser", "email": "newuser@example.com", "password": generate_random_password()}
        response = self.client.post(reverse("signup"), signup_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)

    def test_signup_existing_username(self):
        self.client.credentials()
        signup_data = {
            "username": "testuser",  # Already exists
            "email": "newemail@example.com",
            "password": generate_random_password(),
        }
        response = self.client.post(reverse("signup"), signup_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Username already exists", response.data["message"])

    def test_login_success(self):
        # Ensure the correct credentials are used during login
        login_data = {"username": self.user.username, "password": self.password}  # Use the correct password
        response = self.client.post(reverse("token_obtain_pair"), login_data, format="json")

        # Check if the login was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # Check if the access token is returned

    def test_login_invalid_credentials(self):
        self.client.credentials()
        login_data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(reverse("token_obtain_pair"), login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_success(self):
        refresh_data = {"refresh": str(RefreshToken.for_user(self.user))}
        response = self.client.post(reverse("token_refresh"), refresh_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    # Schedule Tests
    def test_access_without_auth(self):
        self.client.credentials()
        response = self.client.get(reverse("schedule-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_auth(self):
        response = self.client.get(reverse("schedule-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_schedule_success(self):
        response = self.client.post(reverse("schedule-list"), self.valid_schedule_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        schedule = Schedule.objects.first()
        self.assertIsNotNone(schedule)  # Ensure schedule is not None
        if schedule is not None:  # Add this None check
            self.assertEqual(schedule.user, self.user)  # Ensure the schedule is associated with the correct user

    def test_get_all_schedules(self):
        Schedule.objects.create(schedule=self.valid_schedule_data["schedule"], user=self.user)
        response = self.client.get(reverse("schedule-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_schedule_success(self):
        schedule = Schedule.objects.create(schedule=self.valid_schedule_data["schedule"], user=self.user)
        if schedule is not None:
            updated_data = {"schedule": {"wednesday": [{"start": "10:00", "stop": "12:00", "ids": [7, 8]}]}}
            response = self.client.put(reverse("schedule-detail", args=[schedule.id]), updated_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["schedule"]["wednesday"][0]["start"], "10:00")
        else:
            # Handle the case where schedule is None
            pass

    def test_delete_schedule_success(self):
        schedule = Schedule.objects.create(schedule=self.valid_schedule_data["schedule"], user=self.user)
        self.assertIsNotNone(schedule)  # Check that the schedule is not None
        response = self.client.delete(reverse("schedule-detail", args=[schedule.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Schedule.objects.count(), 0)

    # Ownership and Permissions Tests
    def test_access_schedule_of_other_user(self):
        # Create a schedule for the other user
        schedule = Schedule.objects.create(schedule=self.valid_schedule_data["schedule"], user=self.other_user)

        # Try to access the other user's schedule
        response = self.client.get(reverse("schedule-detail", args=[schedule.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Should not find another user's schedule

    def test_update_schedule_of_other_user(self):
        # Create a schedule for the other user
        schedule = Schedule.objects.create(schedule=self.valid_schedule_data["schedule"], user=self.other_user)

        # Try to update the other user's schedule
        updated_data = {"schedule": {"wednesday": [{"start": "10:00", "stop": "12:00", "ids": [7, 8]}]}}
        response = self.client.put(reverse("schedule-detail", args=[schedule.id]), updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Should not update another user's schedule

    def test_delete_schedule_of_other_user(self):
        # Create a schedule for the other user
        schedule = Schedule.objects.create(schedule=self.valid_schedule_data["schedule"], user=self.other_user)

        # Try to delete the other user's schedule
        response = self.client.delete(reverse("schedule-detail", args=[schedule.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Should not delete another user's schedule

    # Validation Tests
    def test_create_schedule_invalid_data(self):
        response = self.client.post(reverse("schedule-list"), self.invalid_schedule_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Each time slot must contain 'start', 'stop', and 'ids' fields.", response.data["schedule"][0])

    def test_create_schedule_invalid_day(self):
        response = self.client.post(reverse("schedule-list"), self.invalid_day_schedule_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid day", response.data["schedule"][0])

    def test_create_schedule_missing_ids(self):
        response = self.client.post(reverse("schedule-list"), self.missing_ids_schedule_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Each time slot must contain 'start', 'stop', and 'ids' fields.", response.data["schedule"][0])

    # Serializer Validation
    def test_validate_valid_schedule(self):
        valid_schedule = {
            "monday": [
                {"start": "08:00", "stop": "10:00", "ids": [1, 2]},
                {"start": "11:00", "stop": "12:00", "ids": [3, 4]},
            ]
        }
        serializer = ScheduleSerializer(data={"schedule": valid_schedule})
        self.assertTrue(serializer.is_valid())

    def test_validate_invalid_schedule_missing_fields(self):
        invalid_schedule = {"monday": [{"stop": "10:00", "ids": [1, 2]}]}
        serializer = ScheduleSerializer(data={"schedule": invalid_schedule})
        self.assertFalse(serializer.is_valid())
        self.assertIn("Each time slot must contain 'start', 'stop', and 'ids' fields.", str(serializer.errors))

    def test_validate_invalid_day_schedule(self):
        invalid_schedule = {"funday": [{"start": "08:00", "stop": "10:00", "ids": [1, 2]}]}
        serializer = ScheduleSerializer(data={"schedule": invalid_schedule})
        self.assertFalse(serializer.is_valid())
        self.assertIn("Invalid day", str(serializer.errors))
