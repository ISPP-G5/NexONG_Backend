from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token


class AdminScheduleApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser", email="example@gmail.com", role=ADMIN
        )
        self.educator = Educator.objects.create(
            description="testdeprueba11", birthdate="2002-04-21"
        )
        self.token = Token.objects.create(user=self.user)

        self.lesson = Lesson.objects.create(
            name="PRIMER CICLO 4",
            description="Módulo VI, segunda planta",
            capacity=16,
            is_morning_lesson=True,
            educator=self.educator,
            start_date="2024-01-28",
            end_date="2024-05-28",
        )

        self.schedule = Schedule.objects.create(
            weekday="MONDAY",
            start_time="12:00:00",
            end_time="13:30:00",
            lesson=self.lesson,
        )

    def test_get_schedule_by_admin(self):
        response = self.client.get(
            f"/api/schedule/{self.schedule.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_schedule_by_admin(self):
        response = self.client.post(
            f"/api/schedule/",
            data={
                "weekday": "LUNES",
                "start_time": "12:00:00",
                "end_time": "13:30:00",
                "lesson": self.lesson.id,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_schedule_error_by_admin(self):
        response = self.client.post(
            f"/api/schedule/",
            data={
                "weekday": "LUNES",
                "start_time": "14:00:00",
                "end_time": "13:30:00",
                "lesson": self.lesson.id,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_schedule_by_admin(self):
        response = self.client.put(
            f"/api/schedule/{self.schedule.id}/",
            data={
                "weekday": "LUNES",
                "start_time": "13:00:00",
                "end_time": "14:30:00",
                "lesson": self.lesson.id,
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
