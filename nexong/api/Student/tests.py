from django.test import TestCase
from nexong.api.Student.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

class StudentApiViewSetTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create(username='testuser')
        # Crear un token de autenticación para el usuario
        self.token = Token.objects.create(user=self.user)

    def test_create_student(self):
        # Contar el número de estudiantes antes de la creación
        numero_estudiantes = Student.objects.count()

        # Crear una familia y un centro educativo
        family = Family.objects.create(name='Familia López')
        education_center = EducationCenter.objects.create(name='San Francisco Solano')

        # Hacer una solicitud POST para crear un estudiante
        response = self.client.post(
            '/api/student/',
            {
            "name": "José",
            "surname": "Algaba",
            "education_center": education_center.id,
            "is_morning_student": True,
            "activities_during_exit": "",
            "status": "ACEPTADO",
            "current_education_year": "TRES AÑOS",
            "education_center_tutor": "Don Carlos Perez",
            "nationality": "España",
            "birthdate": "2017-04-21",
            "family": family.id,
            },
            HTTP_AUTHORIZATION=f'Token {self.token.key}'  # Pasar el token como encabezado de autorización
        )

        # Verificar si la solicitud fue exitosa (status code 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), numero_estudiantes + 1)

        # Obtener el estudiante creado
        student = Student.objects.first()

        # Verificar que los datos del estudiante coincidan con los datos enviados en la solicitud POST
        self.assertEqual(student.name, "José")
        self.assertEqual(student.surname, "Algaba")
    