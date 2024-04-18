from nexong.api.Authentication.views import *
from nexong.api.helpers.testsSetup import testSetupEducator
from nexong.models import *
from rest_framework.test import APITestCase
from rest_framework import status


class EducatorStudentApiViewSetTestCase(APITestCase):
    def setUp(self):
        testSetupEducator(self)
      
    def test_create_student_by_educator(self):
        self.student_data["family"] = self.family.id
        self.student_data["education_center"] = self.education_center.id
        response = self.client.post(
            "/api/student/",
            self.student_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_obtain_student_by_educator(self):
        student = Student.objects.create(**self.student_data)
        response = self.client.get(
            f"/api/student/{student.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Guillermo")

    def test_update_student_by_educator(self):
        student = Student.objects.create(**self.student_data)
        self.student_data["family"] = self.family.id
        self.student_data["education_center"] = self.education_center.id
        self.student_data["name"] = "Jose"
        response = self.client.put(
            f"/api/student/{student.id}/",
            self.student_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_student_by_educator(self):
        student = Student.objects.create(**self.student_data)
        response = self.client.delete(
            f"/api/student/{student.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EducatorQuarterMArksApiViewSetTestCase(APITestCase):
    def setUp(self):
        testSetupEducator(self)

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
        self.assertEqual(response.data["date"], "2024-03-05")

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
