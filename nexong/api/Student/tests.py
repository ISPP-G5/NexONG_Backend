from django.test import TestCase
from nexong.api.Student.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

'''class StudentApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
    
    def test_create_partner(self):
        numero_Estudiantes = Student.objects.count()
        response = self.client.post('/api/student/', {"name": "José",
            "surname": "Algaba",
            "education_center": 1,
            "is_morning_student": True,
            "activities_during_exit": "",
            "status": "ACEPTADO",
            "current_education_year": "TRES AÑOS",
            "education_center_tutor": "Don Carlos Perez",
            "enrollment_document": "student_enrollment\\student_enrollment.txt",
            "scanned_sanitary_card": "student_sanitary\\student_sanitary.txt",
            "nationality" : "España",
            "birthdate" : "2017-04-21",
            "family":1,
            "avatar": "student_avatar\\student_avatar.png"})
        self.assertEqual(response.status_code, 201)
        student = Student.objects.first()
        self.assertEqual(Student.objects.count(), numero_Estudiantes + 1)
        self.assertEqual(student.name, "José")'''
