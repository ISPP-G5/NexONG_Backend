from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


class EducatorStudentApiViewSetTestCase(APITestCase):
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
        self.education_center = EducationCenter.objects.create(
            name="San Francisco Solano"
        )
        self.student = {
            "name": "Amadeo",
            "surname": "Portillo",
            "education_center": self.education_center,
            "is_morning_student": True,
            "activities_during_exit": "",
            "status": "ACEPTADO",
            "current_education_year": "TRES AÑOS",
            "education_center_tutor": "Don Carlos Perez",
            "nationality": "Alemania",
            "birthdate": "2015-04-21",
            "family": self.family,
        }

    def test_create_student_by_educator(self):
        self.student["family"] = self.family.id
        self.student["education_center"] = self.education_center.id
        response = self.client.post(
            "/api/student/",
            self.student,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_obtain_student_by_educator(self):
        student = Student.objects.create(**self.student)
        response = self.client.get(
            f"/api/student/{student.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Amadeo")

    def test_update_student_by_educator(self):
        student = Student.objects.create(**self.student)
        self.student["family"] = self.family.id
        self.student["education_center"] = self.education_center.id
        self.student["name"] = "Jose"
        response = self.client.put(
            f"/api/student/{student.id}/",
            self.student,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_student_by_educator(self):
        student = Student.objects.create(**self.student)
        response = self.client.delete(
            f"/api/student/{student.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EducatorQuarterMArksApiViewSetTestCase(APITestCase):
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
        self.quartermarks = {"date": "2024-03-21", "student": self.student}
        file_content = b"Test file content"
        self.quartermarks["marks"] = SimpleUploadedFile(
            "student_marks.pdf", file_content
        )

    def test_create_quarterMarks_by_educator(self):
        self.quartermarks["student"] = self.student.id
        response = self.client.post(
            "/api/quarter-marks/",
            self.quartermarks,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_obtain_quarterMarks_by_educator(self):
        quartermarks = QuarterMarks.objects.create(**self.quartermarks)
        response = self.client.get(
            f"/api/quarter-marks/{quartermarks.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["date"], "2024-03-21")

    def test_update_quarterMarks_by_educator(self):
        quartermarks = QuarterMarks.objects.create(**self.quartermarks)
        self.quartermarks["student"] = self.student.id
        self.quartermarks["date"] = "2024-03-16"
        response = self.client.put(
            f"/api/quarter-marks/{quartermarks.id}/",
            self.quartermarks,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_quarterMarks_by_educator(self):
        quartermarks = QuarterMarks.objects.create(**self.quartermarks)
        response = self.client.delete(
            f"/api/quarter-marks/{quartermarks.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
