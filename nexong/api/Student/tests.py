from django.test import TestCase
from nexong.api.Student.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.core.files.uploadedfile import SimpleUploadedFile


def add_files_to_student_data(self):
    file_content = b"Test file content"  # Content of the file
    self.student_data["enrollment_document"] = SimpleUploadedFile(
        "enrollment_document.pdf", file_content
    )
    self.student_data["scanned_sanitary_card"] = SimpleUploadedFile(
        "scanned_sanitary_card.pdf", file_content
    )

class StudentApiViewSetTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        educator = Educator.objects.create(birthdate='2000-04-21')
        education = EducationCenter.objects.create(name = 'San Francisco Solano')
        familia = Family.objects.create(name = 'Familia López')
        voluntario = Volunteer.objects.create(
            academic_formation = "Test formation",
            motivation= "Test motivation",
            status="PENDIENTE",
            address="Test address",
            postal_code=12345,
            birthdate = "1956-07-05",
            start_date = "1956-07-05",
            end_date= "1956-07-05"
        )
        self.user = User.objects.create(username='testuser', email = "example@gmail.com")
        self.user2 = User.objects.create(username = 'testuser2', email = "example2@gmail.com", role = EDUCATOR, educator = educator)
        self.user3 = User.objects.create(username = 'testuser3', email = "example3@gmail.com", role = EDUCATION_CENTER, education_center = education)
        self.user4 = User.objects.create(username = 'testuser4', email = "example4@gmail.com", role = FAMILY, family = familia)
        self.user5 = User.objects.create(username='testuser5', email = "example5@gmail.com", role = VOLUNTEER, volunteer = voluntario)

        
        # Crear un token de autenticación para el usuario
        self.token = Token.objects.create(user=self.user)
        self.token2 = Token.objects.create(user = self.user2)
        self.token3 = Token.objects.create(user = self.user3)
        self.token4 = Token.objects.create(user = self.user4)
        self.token5 = Token.objects.create(user = self.user5)

        self.student_data = {
            "name": "José",
            "surname": "Algaba",
            "education_center": education,
            "is_morning_student": True,
            "activities_during_exit": "",
            "status": "ACEPTADO",
            "current_education_year": "TRES AÑOS",
            "education_center_tutor": "Don Carlos Perez",
            "nationality": "España",
            "birthdate": "2017-04-21",
            "family": familia,

        }
        add_files_to_student_data(self)


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

    def test_create_student_name_error(self):
        # Contar el número de estudiantes antes de la creación
        numero_estudiantes = Student.objects.count()

        # Crear una familia y un centro educativo
        family = Family.objects.create(name='Familia López')
        education_center = EducationCenter.objects.create(name='San Francisco Solano')

        # Hacer una solicitud POST para crear un estudiante
        response = self.client.post(
            '/api/student/',
            {
            "name": "",
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_surname_error(self):
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
            "surname": "",
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_birthday_error(self):
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
            "birthdate": "2025-04-21",
            "family": family.id,
            },
            HTTP_AUTHORIZATION=f'Token {self.token3.key}'  # Pasar el token como encabezado de autorización
        )

        # Verificar si la solicitud fue exitosa (status code 201)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_student(self):
        # Crear una familia y un centro educativo
        family = Family.objects.create(name='Familia López')
        education_center = EducationCenter.objects.create(name='San Francisco Solano')
        # Crear un estudiante
        student = Student.objects.create(
            name= "José",
            surname= "Algaba",
            education_center= education_center,
            is_morning_student= True,
            activities_during_exit= "",
            status= "ACEPTADO",
            current_education_year= "TRES AÑOS",
            education_center_tutor= "Don Carlos Perez",
            nationality= "España",
            birthdate= "2017-04-21",
            family= family
        )

        # Autenticar la solicitud GET con el token de autenticación
        response = self.client.get(f'/api/student/{student.id}/', HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        # Verificar que la solicitud fue exitosa (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificar que los datos del estudiante devueltos sean correctos
        self.assertEqual(response.data['name'], 'José')
        self.assertEqual(response.data['surname'], 'Algaba')

    def test_obtain_student_error_id(self):
        # Crear una familia y un centro educativo
        family = Family.objects.create(name='Familia López')
        education_center = EducationCenter.objects.create(name='San Francisco Solano')
        # Crear un estudiante
        student = Student.objects.create(
            name= "José",
            surname= "Algaba",
            education_center= education_center,
            is_morning_student= True,
            activities_during_exit= "",
            status= "ACEPTADO",
            current_education_year= "TRES AÑOS",
            education_center_tutor= "Don Carlos Perez",
            nationality= "España",
            birthdate= "2017-04-21",
            family= family
        )

        # Autenticar la solicitud GET con el token de autenticación
        response = self.client.get(f'/api/student/20/', HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        # Verificar que la solicitud fue exitosa (status code 404)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        


    def test_update_student(self):
        # Create a student
        family = Family.objects.create(name='Familia López')
        education_center = EducationCenter.objects.create(name='San Francisco Solano')
        student = Student.objects.create(
            name= "José",
            surname= "Algaba",
            education_center= education_center,
            is_morning_student= True,
            activities_during_exit= "",
            status= "ACEPTADO",
            current_education_year= "TRES AÑOS",
            education_center_tutor= "Don Carlos Perez",
            nationality= "España",
            birthdate= "2017-04-21",
            family= family)

        # Authenticate the PUT request with the authentication token
        response = self.client.put(
            f'/api/student/{student.id}/',
            data = {
            "name": "José",
            "surname": "Algaba",
            "education_center": education_center.id,
            "is_morning_student": True,
            "activities_during_exit": "",
            "status": "ACEPTADO",
            "current_education_year": "TRES AÑOS",
            "education_center_tutor": "Don José Perez",
            "nationality": "España",
            "birthdate": "2017-04-21",
            "family": family.id,

            }, content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.token2.key}'
            
        )
        # Verify that the request was successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_student(self):
        student = Student.objects.create(**self.student_data)
        response = self.client.delete(f"/api/student/{student.id}/",HTTP_AUTHORIZATION=f'Token {self.token3.key}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0) 

    def test_update_student_error_auth(self):
        # Create a student
        family = Family.objects.create(name='Familia Ruz')
        education_center = EducationCenter.objects.create(name='San Francisco Solano')
        student = Student.objects.create(
            name= "José",
            surname= "Algaba",
            education_center= education_center,
            is_morning_student= True,
            activities_during_exit= "",
            status= "ACEPTADO",
            current_education_year= "TRES AÑOS",
            education_center_tutor= "Don Carlos Perez",
            nationality= "España",
            birthdate= "2017-04-21",
            family= family)

        # Authenticate the PUT request with the authentication token
        response = self.client.put(
            f'/api/student/{student.id}/',
            data = {
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

            }, content_type='application/json',HTTP_AUTHORIZATION=f'Token {self.token5.key}'
            
        )
        

        # Verify that the request was successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Verify that the returned student data is correct

    def test_delete_student_error_auth(self):
            student = Student.objects.create(**self.student_data)
            response = self.client.delete(f"/api/student/{student.id}/",HTTP_AUTHORIZATION=f'Token {self.token5.key}')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(Student.objects.count(), 1)

    def test_delete_student_error_id(self):
            response = self.client.delete(f"/api/student/20/",HTTP_AUTHORIZATION=f'Token {self.token3.key}')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
   

    
    

        
    