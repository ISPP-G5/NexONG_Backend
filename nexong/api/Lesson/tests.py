from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from nexong.api.helpers.testsSetup import testSetupEducator


class AdminLessonApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser", email="example@gmail.com", role=ADMIN
        )
        self.family = Family.objects.create(name="Familia Pedraza")
        self.education_center = EducationCenter.objects.create(
            name="San Francisco Solano"
        )
        self.token = Token.objects.create(user=self.user)
        self.educator = Educator.objects.create(
            description="testdeprueba7", birthdate="2002-04-21"
        )
        self.lesson = Lesson.objects.create(
            name="PRIMER CICLO 2",
            description="Módulo V, segunda planta",
            capacity=16,
            is_morning_lesson=True,
            educator=self.educator,
            start_date="2024-01-28",
            end_date="2024-05-28",
        )
        self.student = Student.objects.create(
            name="Antonio Manuel",
            surname="Carmona",
            education_center=self.education_center,
            is_morning_student=True,
            activities_during_exit="",
            status="ACEPTADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Sebastian Perez",
            nationality="Francia",
            birthdate="2017-04-21",
            family=self.family,
        )
        self.student2 = Student.objects.create(
            name="Andrés Francisco",
            surname="Montes",
            education_center=self.education_center,
            is_morning_student=True,
            activities_during_exit="",
            status="PENDIENTE",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Sebastian Perez",
            nationality="España",
            birthdate="2015-04-21",
            family=self.family,
        )
        self.volunteer = Volunteer.objects.create(
            academic_formation="Volunteer Admin ",
            motivation="Volunteer Admin",
            status="ACEPTADO",
            address="Volunteer Admin",
            postal_code=12350,
            birthdate="1957-07-05",
            start_date="1960-07-05",
            end_date="1980-07-05",
        )
        self.lesson_attendance = LessonAttendance.objects.create(
            date="2025-04-21", lesson=self.lesson, volunteer=self.volunteer
        )

    def test_obtain_lesson_by_admin(self):
        response = self.client.get(
            f"/api/lesson/{self.lesson.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_create_lesson_by_admin(self):
        attendees_ids = [self.student.id, self.student2.id]
        response = self.client.post(
            f"/api/lesson/",
            data={
                "name": "SEGUNDO CICLO 2",
                "description": "Módulo VI, segunda planta",
                "capacity": 16,
                "is_morning_lesson": True,
                "educator": self.educator.id,
                "students": attendees_ids,
                "start_date": "2025-12-10",
                "end_date": "2025-12-11",
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_date_error_by_admin(self):
        attendees_ids = [self.student.id, self.student2.id]
        response = self.client.post(
            f"/api/lesson/",
            data={
                "name": "Sector 3",
                "description": "Módulo VII, segunda planta",
                "capacity": 18,
                "is_morning_lesson": True,
                "educator": self.educator.id,
                "students": attendees_ids,
                "start_date": "2023-12-10",
                "end_date": "2023-12-11",
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_lesson_date2_error_by_admin(self):
        attendees_ids = [self.student.id, self.student2.id]
        response = self.client.post(
            f"/api/lesson/",
            data={
                "name": "Sector 33",
                "description": "Módulo 59",
                "capacity": 16,
                "is_morning_lesson": False,
                "educator": self.educator.id,
                "students": attendees_ids,
                "start_date": "2025-12-11",
                "end_date": "2025-12-10",
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_lesson_by_admin(self):
        attendees_ids = [self.student.id, self.student2.id]
        response = self.client.put(
            f"/api/lesson/{self.lesson.id}/",
            data={
                "name": "SEGUNDO CICLO 2",
                "description": "Módulo VI, segunda planta",
                "capacity": 16,
                "is_morning_lesson": True,
                "educator": self.educator.id,
                "students": attendees_ids,
                "start_date": "2025-12-10",
                "end_date": "2025-12-11",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_date_error_by_admin(self):
        attendees_ids = [self.student.id, self.student2.id]
        response = self.client.put(
            f"/api/lesson/{self.lesson.id}/",
            data={
                "name": "SEGUNDO CICLO 2",
                "description": "Módulo VI, segunda planta",
                "capacity": 16,
                "is_morning_lesson": True,
                "educator": self.educator.id,
                "students": attendees_ids,
                "start_date": "2023-12-10",
                "end_date": "2023-12-11",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_lesson_date2_error_by_admin(self):
        attendees_ids = [self.student.id, self.student2.id]
        response = self.client.put(
            f"/api/lesson/{self.lesson.id}/",
            data={
                "name": "Ciclo Carpinteria",
                "description": "Módulo 33",
                "capacity": 33,
                "is_morning_lesson": True,
                "educator": self.educator.id,
                "students": attendees_ids,
                "start_date": "2025-12-11",
                "end_date": "2025-12-10",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_lesson_by_admin(self):
        response = self.client.delete(
            f"/api/lesson/{self.lesson.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_obtain_lesson_attendance_by_admin(self):
        response = self.client.get(
            f"/api/lesson-attendance/{self.lesson_attendance.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_lesson_attendance_by_admin(self):
        response = self.client.delete(
            f"/api/lesson-attendance/{self.lesson_attendance.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 204)


class EducatorLessonApiViewSetTestCase(APITestCase):
    def setUp(self):
        testSetupEducator(self)

    def test_create_lesson_by_educator(self):
        self.lesson_data["educator"] = self.educator.id
        response = self.client.post(
            "/api/lesson/",
            self.lesson_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_obtain_lesson_by_educator(self):
        lesson = Lesson.objects.create(**self.lesson_data)
        response = self.client.get(
            f"/api/lesson/{lesson.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Filosofia")

    def test_update_lesson_by_educator(self):
        lesson = Lesson.objects.create(**self.lesson_data)
        self.lesson_data["educator"] = self.educator.id
        self.lesson_data["is_morning_lesson"] = False
        response = self.client.put(
            f"/api/lesson/{lesson.id}/",
            self.lesson_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_by_educator(self):
        lesson = Lesson.objects.create(**self.lesson_data)
        response = self.client.delete(
            f"/api/lesson/{lesson.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EducatorLessonAttendanceApiViewSetTestCase(APITestCase):
    def setUp(self):
        testSetupEducator(self)

    def test_create_lessonAttendance_by_educator(self):
        self.lessonAtendance_data["lesson"] = self.lesson.id
        self.lessonAtendance_data["volunteer"] = self.volunteer.id
        response = self.client.post(
            "/api/lesson-attendance/",
            self.lessonAtendance_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_obtain_lessonAttendance_by_educator(self):
        lessonAttendance = LessonAttendance.objects.create(**self.lessonAtendance_data)
        response = self.client.get(
            f"/api/lesson-attendance/{lessonAttendance.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["date"], "2024-02-23")

    def test_update_lessonAttendance_by_educator(self):
        lessonAttendance = LessonAttendance.objects.create(**self.lessonAtendance_data)
        self.lessonAtendance_data["lesson"] = self.lesson.id
        self.lessonAtendance_data["volunteer"] = self.volunteer.id
        self.lessonAtendance_data["date"] = "2024-01-20"

        response = self.client.put(
            f"/api/lesson-attendance/{lessonAttendance.id}/",
            self.lessonAtendance_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lessonAttendance_by_educator(self):
        lessonAttendance = LessonAttendance.objects.create(**self.lessonAtendance_data)
        response = self.client.delete(
            f"/api/lesson-attendance/{lessonAttendance.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
