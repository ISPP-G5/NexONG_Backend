from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APITestCase
from rest_framework import status
from nexong.api.helpers.testsSetup import testSetupEducator


class EducatorEvaluationTypeTestCase(APITestCase):
    def setUp(self):
        testSetupEducator(self)

    def test_create_evaluation_type_by_educator(self):
        self.evaluation_type_data["lesson"] = self.lesson.id
        self.evaluation_type_data_bad_request["lesson"] = self.lesson.id
        response = self.client.post(
            "/api/evaluation-type/",
            self.evaluation_type_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(
            "/api/evaluation-type/",
            self.evaluation_type_data_bad_request,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_evaluation_type_by_educator(self):
        eval_type = EvaluationType.objects.create(**self.evaluation_type_data)
        eval_type_forbid = EvaluationType.objects.create(
            **self.evaluation_type_data_forbiden
        )
        response = self.client.get(
            f"/api/evaluation-type/{eval_type.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Asistencia")
        self.assertEqual(response.data["description"], "asitencia diaria")

        response2 = self.client.get(
            f"/api/evaluation-type/{eval_type_forbid.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_evaluation_type_by_educator(self):
        eval_type = EvaluationType.objects.create(**self.evaluation_type_data)
        self.evaluation_type_data["name"] = "Participacion en clase"
        self.evaluation_type_data["lesson"] = self.lesson.id
        self.evaluation_type_data_bad_request["lesson"] = self.lesson.id

        response = self.client.put(
            f"/api/evaluation-type/{eval_type.id}/",
            self.evaluation_type_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Participacion en clase")

        eval_type_forbid = EvaluationType.objects.create(
            **self.evaluation_type_data_forbiden
        )
        self.evaluation_type_data_forbiden["lesson"] = self.lesson2.id
        response2 = self.client.put(
            f"/api/evaluation-type/{eval_type_forbid.id}/",
            self.evaluation_type_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

        response3 = self.client.put(
            f"/api/evaluation-type/{eval_type.id}/",
            self.evaluation_type_data_bad_request,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_evaluation_type_by_educator(self):
        eval_type = EvaluationType.objects.create(**self.evaluation_type_data)
        eval_type_forbid = EvaluationType.objects.create(
            **self.evaluation_type_data_forbiden
        )
        count = EvaluationType.objects.count()
        response = self.client.delete(
            f"/api/evaluation-type/{eval_type.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        response2 = self.client.delete(
            f"/api/evaluation-type/{eval_type_forbid.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EvaluationType.objects.count(), count - 1)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)


class EducatorStudentEvaluationTestCase(APITestCase):
    def setUp(self):
        testSetupEducator(self)

    def test_create_student_evaluation_by_educator(self):
        self.student_eval_data["student"] = self.student.id
        self.student_eval_data["evaluation_type"] = self.evaluation_type.id
        self.student_eval_data_bad_request["student"] = self.student.id
        self.student_eval_data_bad_request["evaluation_type"] = self.evaluation_type2.id
        response = self.client.post(
            "/api/student-evaluation/",
            self.student_eval_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(
            "/api/student-evaluation/",
            self.student_eval_data_bad_request,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_student_evaluation_by_educator(self):
        student_eval = StudentEvaluation.objects.create(**self.student_eval_data)
        student_eval_forbid = StudentEvaluation.objects.create(
            **self.student_eval_data_forbiden
        )
        response = self.client.get(
            f"/api/student-evaluation/{student_eval.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["grade"], 0)
        self.assertEqual(response.data["comment"], "Puede mejorar")

        response2 = self.client.get(
            f"/api/student-evaluation/{student_eval_forbid.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_student_evaluation_by_educator(self):
        student_eval = StudentEvaluation.objects.create(**self.student_eval_data)
        self.student_eval_data["student"] = self.student.id
        self.student_eval_data["evaluation_type"] = self.evaluation_type.id
        self.student_eval_data["comment"] = "Mejoro tras la revision"

        response = self.client.put(
            f"/api/student-evaluation/{student_eval.id}/",
            self.student_eval_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["comment"], "Mejoro tras la revision")

        student_eval_forbid = StudentEvaluation.objects.create(
            **self.student_eval_data_forbiden
        )
        self.student_eval_data_forbiden["student"] = self.student.id
        self.student_eval_data_forbiden["evaluation_type"] = self.evaluation_type2.id
        response2 = self.client.put(
            f"/api/student-evaluation/{student_eval_forbid.id}/",
            self.student_eval_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

        response3 = self.client.put(
            f"/api/student-evaluation/{student_eval.id}/",
            self.student_eval_data_bad_request,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_student_evaluation_by_educator(self):
        student_eval = StudentEvaluation.objects.create(**self.student_eval_data)
        student_eval_forbid = StudentEvaluation.objects.create(
            **self.student_eval_data_forbiden
        )
        response = self.client.delete(
            f"/api/student-evaluation/{student_eval.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        response2 = self.client.delete(
            f"/api/student-evaluation/{student_eval_forbid.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(StudentEvaluation.objects.count(), 1)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
