from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory


class Lesson_ApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.family = Family.objects.create(name="Familia Garcia")
        self.education_center = EducationCenter.objects.create(
            name="San Francisco Asis"
        )
        self.educator = Educator.objects.create(birthdate="2002-04-21")
        self.user = User.objects.create(
            username="testuser",
            email="example@gmail.com",
            role=FAMILY,
            family=self.family,
        )
        self.token = Token.objects.create(user=self.user)

    def test_obtain_lesson_by_family(self):
        lesson = Lesson.objects.create(
            name="PRIMER CICLO 2",
            description="Módulo III, segunda planta",
            capacity=16,
            is_morning_lesson=True,
            educator=self.educator,
            start_date="2024-01-28",
            end_date="2024-05-28",
        )
        response = self.client.get(
            f"/api/lesson/{lesson.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_create_lesson_by_family_error(self):
        response = self.client.post(
            f"/api/lesson/",
            data={
                "name": "PRIMER CICLO 2",
                "description": "Módulo III, tercera planta",
                "capacity": 14,
                "is_morning_lesson": True,
                "educator": self.educator,
                "start_date": "2024-01-28",
                "end_date": "2024-06-28",
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_student_evaluation_permissions_error(self):
        lesson_delete = Lesson.objects.create(
            name="PRIMER CICLO 2",
            description="Módulo IV, segunda planta",
            capacity=16,
            is_morning_lesson=False,
            educator=self.educator,
            start_date="2024-01-28",
            end_date="2024-05-28",
        )
        response = self.client.delete(
            f"/api/student-evaluation/{lesson_delete.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
