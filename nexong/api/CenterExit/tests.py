from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
import base64


class CenterExitApiViewSetTestCase(TestCase):
    def setUp(self):
        self.family = Family.objects.create(name="Familia López")
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser",
            email="example@gmail.com",
            role=FAMILY,
            family=self.family,
        )
        self.user2 = User.objects.create(
            username="testuser2", email="example2@gmail.com", role=ADMIN
        )
        self.token = Token.objects.create(user=self.user)
        self.token2 = Token.objects.create(user=self.user2)
        file_content = b"Test file content"
        self.authorization = SimpleUploadedFile(
            "centerexit_authorization.pdf", file_content
        )
        self.educator = Educator.objects.create(birthdate="2000-04-21")
        self.educator2 = Educator.objects.create(birthdate="2000-04-22")
        self.education_center = EducationCenter.objects.create(
            name="San Francisco Solano"
        )
        self.voluntario = Volunteer.objects.create(
            academic_formation="Test formation",
            motivation="Test motivation",
            status="ACEPTADO",
            address="Test address",
            postal_code=12345,
            birthdate="1956-07-05",
            start_date="1956-07-05",
            end_date="1956-07-05",
        )
        self.voluntario2 = Volunteer.objects.create(
            academic_formation="Test formation2",
            motivation="Test motivation2",
            status="ACEPTADO",
            address="Test address",
            postal_code=12345,
            birthdate="1956-07-05",
            start_date="1956-07-05",
            end_date="1956-07-05",
        )
        self.student = Student.objects.create(
            name="Amadeo",
            surname="Portillo",
            education_center=self.education_center,
            is_morning_student=True,
            activities_during_exit="",
            status="ACEPTADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Carlos Perez",
            nationality="Alemania",
            birthdate="2015-04-21",
            family=self.family,
        )
        self.student2 = Student.objects.create(
            name="Pablo",
            surname="Portillo",
            education_center=self.education_center,
            is_morning_student=True,
            activities_during_exit="",
            status="ACEPTADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Carlos Perez",
            nationality="Alemania",
            birthdate="2015-04-21",
            family=self.family,
        )
        self.lesson = Lesson.objects.create(
            name="PRIMER CICLO 1",
            description="Módulo I, segunda planta",
            capacity=4,
            is_morning_lesson=True,
            educator=self.educator,
            start_date="2024-01-28",
            end_date="2024-05-28",
        )
        self.lesson_event = LessonEvent.objects.create(
            name="Excursión a La Giralda",
            description="Vamos al centro a ver La Giralda",
            place="Centro Sevilla",
            price=25,
            max_volunteers=10,
            start_date="2024-04-18 12:00-00:00",
            end_date="2024-04-18 18:00-00:00",
            lesson=self.lesson,
        )
        self.lesson_event.educators.add(self.educator, self.educator2)
        self.lesson_event.attendees.add(self.student, self.student2)
        self.lesson_event.volunteers.add(self.voluntario, self.voluntario2)

        self.center_exit = {
            "student": self.student,
            "is_authorized": True,
            "lesson_event": self.lesson_event,
        }

    def test_create_center_exit(self):
        center_exit_creadas = CenterExitAuthorization.objects.count()
        response = self.client.post(
            "/api/center-exit/",
            {
                "authorization": self.authorization,
                "student": self.student.id,
                "is_authorized": True,
                "lesson_event": self.lesson_event.id,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        print(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            CenterExitAuthorization.objects.count(), center_exit_creadas + 1
        )
        center_exit = CenterExitAuthorization.objects.first()
        self.assertEqual(center_exit.is_authorized, True)

    def test_obtain_center_authorization(self):
        center_exit = CenterExitAuthorization.objects.create(
            authorization=self.authorization,
            student=self.student,
            is_authorized=True,
            lesson_event=self.lesson_event,
        )
        response = self.client.get(
            f"/api/center-exit/{center_exit.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(center_exit.is_authorized, True)

    def test_delete_center_authorization(self):
        center_exit1 = CenterExitAuthorization.objects.create(
            authorization=self.authorization,
            student=self.student,
            is_authorized=False,
            lesson_event=self.lesson_event,
        )
        initial_count = CenterExitAuthorization.objects.count()
        response = self.client.delete(
            f"/api/center-exit/{center_exit1.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(CenterExitAuthorization.objects.count(), initial_count - 1)
