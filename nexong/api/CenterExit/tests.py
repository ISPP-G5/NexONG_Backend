from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


class EducatorCenterExitApiViewSetTestCase(APITestCase):
    def setUp(self):
        self.family = Family.objects.create(name="Los Pedraz")
        self.educator = Educator.objects.create(
            birthdate="1969-06-09", description="EL profesor de lengua"
        )
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser",
            email="example@gmail.com",
            role=EDUCATOR,
            educator=self.educator,
        )
        self.token = Token.objects.create(user=self.user)
        self.educator2 = Educator.objects.create(birthdate="2000-04-21")
        self.educator3 = Educator.objects.create(birthdate="2000-04-22")
        self.education_center = EducationCenter.objects.create(
            name="San Francisco Solano"
        )
        self.voluntario = Volunteer.objects.create(
            academic_formation="Prueba Voluntario",
            motivation="Test voluntario",
            status="ACEPTADO",
            address="Test voluntario address",
            postal_code=12359,
            birthdate="1956-07-05",
            start_date="1955-07-05",
            end_date="1956-07-05",
        )
        self.voluntario2 = Volunteer.objects.create(
            academic_formation="Test vol2",
            motivation="Test vol",
            status="ACEPTADO",
            address="Test advol",
            postal_code=12356,
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
            is_morning_student=False,
            activities_during_exit="",
            status="ACEPTADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Carlos Perez",
            nationality="Alemania",
            birthdate="2015-06-21",
            family=self.family,
        )
        self.lesson = Lesson.objects.create(
            name="PRIMER Materia",
            description="Módulo C, segunda planta",
            capacity=50,
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
        self.lesson_event.educators.add(self.educator2, self.educator3)
        self.lesson_event.attendees.add(self.student, self.student2)
        self.lesson_event.volunteers.add(self.voluntario, self.voluntario2)

        self.center_exit = {
            "student": self.student,
            "is_authorized": True,
            "lesson_event": self.lesson_event,
        }
        file_content = b"Test file content"
        self.center_exit["authorization"] = SimpleUploadedFile(
            "centerexit_authorization.pdf", file_content
        )

    def test_create_center_exit_by_educator(self):
        response = self.client.post(
            "/api/center-exit/",
            self.center_exit,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_obtain_center_authorization_by_educator(self):
        center_exit = CenterExitAuthorization.objects.create(**self.center_exit)
        response = self.client.get(
            f"/api/center-exit/{center_exit.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(center_exit.is_authorized, True)

    def test_update_center_authorization_by_educator(self):
        center_exit = CenterExitAuthorization.objects.create(**self.center_exit)
        self.center_exit["is_authorized"] = False
        response = self.client.put(
            f"/api/center-exit/{center_exit.id}/",
            self.center_exit,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_center_authorization_by_educator(self):
        center_exit = CenterExitAuthorization.objects.create(**self.center_exit)
        response = self.client.delete(
            f"/api/center-exit/{center_exit.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
