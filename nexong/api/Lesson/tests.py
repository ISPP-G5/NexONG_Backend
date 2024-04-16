from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status

class EducatorLessonApiViewSetTestCase(APITestCase):
    def setUp(self):
        self.family = Family.objects.create(name="Los Pedraz")
        self.educator = Educator.objects.create(birthdate="1969-06-09", description="EL profesor de lengua")
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser",
            email="example@gmail.com",
            role=EDUCATOR,
            educator=self.educator,
        )
        self.token = Token.objects.create(user=self.user)
        self.education_center = EducationCenter.objects.create(
            name="San Francisco Solano"
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
        self.lesson = {
            "name" :"Primera Materia",
            "description" : "Módulo C, segunda planta",
            "capacity":50,
            "is_morning_lesson":True,
            "educator":self.educator,
            "start_date": "2024-01-28",
            "end_date": "2024-05-28",
        }


    def test_create_lesson_by_educator(self):
        self.lesson["educator"] = self.educator.id
        response = self.client.post(
            "/api/lesson/",
            self.lesson,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_obtain_lesson_by_educator(self):
        lesson = Lesson.objects.create(**self.lesson)
        response = self.client.get(
            f"/api/lesson/{lesson.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Primera Materia")

    def test_update_lesson_by_educator(self):
        lesson = Lesson.objects.create(**self.lesson)
        self.lesson["educator"] = self.educator.id
        self.lesson["is_morning_lesson"] = False
        response = self.client.put(
            f"/api/lesson/{lesson.id}/",
            self.lesson,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_lesson_by_educator(self):
        lesson = Lesson.objects.create(**self.lesson)
        response = self.client.delete(
            f"/api/lesson/{lesson.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class EducatorLessonAttendanceApiViewSetTestCase(APITestCase):
    def setUp(self):
        self.family = Family.objects.create(name="Los Pedraz")
        self.educator = Educator.objects.create(birthdate="1969-06-09", description="EL profesor de lengua")
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser",
            email="example@gmail.com",
            role=EDUCATOR,
            educator=self.educator,
        )
        self.token = Token.objects.create(user=self.user)
        self.education_center = EducationCenter.objects.create(
            name="San Francisco Solano"
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
        self.volunteer = Volunteer.objects.create(
            academic_formation="Prueba Voluntario",
            motivation="Test voluntario",
            status="ACEPTADO",
            address="Test voluntario address",
            postal_code=12359,
            birthdate="1956-07-05",
            start_date="1955-07-05",
            end_date="1956-07-05",
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
        self.lessonAtendance = {
            "date": "2024-01-28",
            "lesson": self.lesson,
            "volunteer": self.volunteer,
        }


    def test_create_lessonAttendance_by_educator(self):
        self.lessonAtendance["lesson"] = self.lesson.id
        self.lessonAtendance["volunteer"] = self.volunteer.id
        response = self.client.post(
            "/api/lesson-attendance/",
            self.lessonAtendance,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_obtain_lessonAttendance_by_educator(self):
        lessonAttendance = LessonAttendance.objects.create(**self.lessonAtendance)
        response = self.client.get(
            f"/api/lesson-attendance/{lessonAttendance.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["date"], "2024-01-28")

    def test_update_lessonAttendance_by_educator(self):
        lessonAttendance = LessonAttendance.objects.create(**self.lessonAtendance)
        self.lessonAtendance["lesson"] = self.lesson.id
        self.lessonAtendance["volunteer"] = self.volunteer.id
        self.lessonAtendance["date"] = "2024-01-20"

        response = self.client.put(
            f"/api/lesson-attendance/{lessonAttendance.id}/",
            self.lessonAtendance,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_lessonAttendance_by_educator(self):
        lessonAttendance = LessonAttendance.objects.create(**self.lessonAtendance)
        response = self.client.delete(
            f"/api/lesson-attendance/{lessonAttendance.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       