from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory


class Student_Evaluation_ApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.family = Family.objects.create(name="Familia Ruz")
        self.education_center = EducationCenter.objects.create(
            name="San Francisco Solano"
        )
        self.educator = Educator.objects.create(birthdate="2000-04-21")
        self.user = User.objects.create(
            username="testuser",
            email="example@gmail.com",
            role=FAMILY,
            family=self.family,
        )
        self.token = Token.objects.create(user=self.user)

        self.student = Student.objects.create(
            name="Alvaro",
            surname="Mejias",
            education_center=self.education_center,
            is_morning_student=True,
            activities_during_exit="",
            status="ACEPTADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Sebastian Perez",
            nationality="España",
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
        self.evaluation_type = EvaluationType.objects.create(
            name="Asistencia diaria",
            description="Campo Prueba",
            evaluation_type="DIARIO",
            grade_system="CERO A UNO",
            lesson=self.lesson,
        )

    def test_obtain_student_evaluation_by_family(self):
        student_evaluation = StudentEvaluation.objects.create(
            grade=8,
            date="2024-02-17",
            comment="Muy bien",
            evaluation_type=self.evaluation_type,
            student=self.student,
        )
        response = self.client.get(
            f"/api/student-evaluation/{student_evaluation.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_create_student_evaluation_by_family_error(self):
        response = self.client.post(
            f"/api/student-evaluation/",
            data={
                "grade": 8,
                "date": "2024-02-17",
                "comment": "Muy bien",
                "evaluation_type": self.evaluation_type.id,
                "student": self.student.id,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_student_evaluation_permissions_error(self):
        student_evaluation = StudentEvaluation.objects.create(
            grade=8,
            date="2024-02-17",
            comment="Muy bien",
            evaluation_type=self.evaluation_type,
            student=self.student,
        )
        response = self.client.put(
            f"/api/student-evaluation/{student_evaluation.id}/",
            data={
                "grade": 5,
                "date": "2024-02-17",
                "comment": "Muy bien",
                "evaluation_type": self.evaluation_type.id,
                "student": self.student.id,
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_student_evaluation_permissions_error(self):
        student_evaluation2 = StudentEvaluation.objects.create(
            grade=4,
            date="2024-02-17",
            comment="Muy bien",
            evaluation_type=self.evaluation_type,
            student=self.student,
        )
        response = self.client.delete(
            f"/api/student-evaluation/{student_evaluation2.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
