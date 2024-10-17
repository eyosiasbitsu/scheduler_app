from typing import Any

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Schedule
from .serializers import ScheduleSerializer


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
        self.user = User.objects.create_user(username="testuser", password="password")  # noqa
        tokens = get_tokens_for_user(self.user)
        self.access_token = tokens["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

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

    # Tests for the authentication endpoints
    def test_signup_success(self):
        self.client.credentials()  # No auth token required for signup
        signup_data = {"username": "newuser", "email": "newuser@example.com", "password": "newpassword123"}
        response = self.client.post(reverse("signup"), signup_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)

    def test_signup_existing_username(self):
        self.client.credentials()
        signup_data = {
            "username": "testuser",  # Already exists
            "email": "newemail@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(reverse("signup"), signup_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Username already exists", response.data["message"])

    def test_login_success(self):
        self.client.credentials()  # No auth token required for login
        login_data = {"username": "testuser", "password": "password"}
        response = self.client.post(reverse("token_obtain_pair"), login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

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

    # Schedule tests
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
        self.assertEqual(Schedule.objects.count(), 1)

    def test_get_all_schedules(self):
        Schedule.objects.create(schedule=self.valid_schedule_data["schedule"])
        response = self.client.get(reverse("schedule-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_schedule_success(self):
        schedule = Schedule.objects.create(schedule=self.valid_schedule_data["schedule"])
        updated_data = {"schedule": {"wednesday": [{"start": "10:00", "stop": "12:00", "ids": [7, 8]}]}}
        response = self.client.put(reverse("schedule-detail", args=[schedule.id]), updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["schedule"]["wednesday"][0]["start"], "10:00")

    def test_delete_schedule_success(self):
        schedule = Schedule.objects.create(schedule=self.valid_schedule_data["schedule"])
        response = self.client.delete(reverse("schedule-detail", args=[schedule.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Schedule.objects.count(), 0)

    def test_create_schedule_without_auth(self):
        self.client.credentials()
        response = self.client.post(reverse("schedule-list"), self.valid_schedule_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_schedule_without_auth(self):
        schedule = Schedule.objects.create(schedule=self.valid_schedule_data["schedule"])
        updated_data = {"schedule": {"wednesday": [{"start": "10:00", "stop": "12:00", "ids": [7, 8]}]}}
        self.client.credentials()
        response = self.client.put(reverse("schedule-detail", args=[schedule.id]), updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_schedule_without_auth(self):
        schedule = Schedule.objects.create(schedule=self.valid_schedule_data["schedule"])
        self.client.credentials()
        response = self.client.delete(reverse("schedule-detail", args=[schedule.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
