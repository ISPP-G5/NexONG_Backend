from django.test import TestCase
from nexong.api.Student.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework import status
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
        self.educator = Educator.objects.create(birthdate="2000-04-21")
        self.education = EducationCenter.objects.create(name="San Francisco Solano")
        self.family = Family.objects.create(name="Familia López")
        voluntario = Volunteer.objects.create(
            academic_formation="Test formation",
            motivation="Test motivation",
            status="PENDIENTE",
            address="Test address",
            postal_code=12345,
            birthdate="1956-07-05",
            start_date="1956-07-05",
            end_date="1956-07-05",
        )
        self.user = User.objects.create(username="testuser", email="example@gmail.com")
        self.user2 = User.objects.create(
            username="testuser2",
            email="example2@gmail.com",
            role=EDUCATOR,
            educator=self.educator,
        )
        self.user3 = User.objects.create(
            username="testuser3",
            email="example3@gmail.com",
            role=EDUCATION_CENTER,
            education_center=self.education,
        )
        self.user4 = User.objects.create(
            username="testuser4",
            email="example4@gmail.com",
            role=FAMILY,
            family=self.family,
        )
        self.user5 = User.objects.create(
            username="testuser5",
            email="example5@gmail.com",
            role=VOLUNTEER,
            volunteer=voluntario,
        )
        self.user6 = User.objects.create(
            username="testuser6", email="example6@gmail.com", role=ADMIN
        )

        # Crear un token de autenticación para el usuario
        self.token = Token.objects.create(user=self.user)
        self.token2 = Token.objects.create(user=self.user2)
        self.token3 = Token.objects.create(user=self.user3)
        self.token4 = Token.objects.create(user=self.user4)
        self.token5 = Token.objects.create(user=self.user5)
        self.token6 = Token.objects.create(user=self.user6)

        self.student_data = {
            "name": "José",
            "surname": "Algaba",
            "education_center": self.education,
            "is_morning_student": True,
            "activities_during_exit": "",
            "status": "ACEPTADO",
            "current_education_year": "TRES AÑOS",
            "education_center_tutor": "Don Carlos Perez",
            "nationality": "España",
            "birthdate": "2017-04-21",
            "family": self.family,
        }
        add_files_to_student_data(self)

    def test_create_student(self):
        # Contar el número de estudiantes antes de la creación
        numero_estudiantes = Student.objects.count()
        # Hacer una solicitud POST para crear un estudiante
        response = self.client.post(
            "/api/student/",
            {
                "name": "Alvaro ",
                "surname": "Rodriguez",
                "education_center": self.education.id,
                "is_morning_student": False,
                "activities_during_exit": "",
                "status": "ACEPTADO",
                "current_education_year": "TRES AÑOS",
                "education_center_tutor": "Don Javier Perez",
                "nationality": "España",
                "birthdate": "2015-04-21",
                "family": self.family.id,
            },
            HTTP_AUTHORIZATION=f"Token {self.token4.key}",  # Pasar el token como encabezado de autorización
        )

        # Verificar si la solicitud fue exitosa (status code 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), numero_estudiantes + 1)

        # Obtener el estudiante creado
        student = Student.objects.first()

        # Verificar que los datos del estudiante coincidan con los datos enviados en la solicitud POST
        self.assertEqual(student.name, "Alvaro")
        self.assertEqual(student.surname, "Rodriguez")

    def test_create_student_name_error(self):
        # Hacer una solicitud POST para crear un estudiante
        response = self.client.post(
            "/api/student/",
            {
                "name": "",
                "surname": "Ruiz",
                "education_center": self.education.id,
                "is_morning_student": True,
                "activities_during_exit": "",
                "status": "ACEPTADO",
                "current_education_year": "TRES AÑOS",
                "education_center_tutor": "Don AdolfoSS Perez",
                "nationality": "Francia",
                "birthdate": "2017-04-21",
                "family": self.family.id,
            },
            HTTP_AUTHORIZATION=f"Token {self.token4.key}",  # Pasar el token como encabezado de autorización
        )

        # Verificar si la solicitud fue exitosa (status code 201)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_surname_error(self):
        # Hacer una solicitud POST para crear un estudiante
        response = self.client.post(
            "/api/student/",
            {
                "name": "Manuel",
                "surname": "",
                "education_center": self.education.id,
                "is_morning_student": False,
                "activities_during_exit": "",
                "status": "ACEPTADO",
                "current_education_year": "TRES AÑOS",
                "education_center_tutor": "Don Carlos Perez",
                "nationality": "Italia",
                "birthdate": "2017-04-21",
                "family": self.family.id,
            },
            HTTP_AUTHORIZATION=f"Token {self.token4.key}",  # Pasar el token como encabezado de autorización
        )

        # Verificar si la solicitud fue exitosa (status code 201)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_birthday_error(self):
        # Hacer una solicitud POST para crear un estudiante
        response = self.client.post(
            "/api/student/",
            {
                "name": "Andrés",
                "surname": "Hurtado",
                "education_center": self.education.id,
                "is_morning_student": False,
                "activities_during_exit": "",
                "status": "ACEPTADO",
                "current_education_year": "TRES AÑOS",
                "education_center_tutor": "Don Mariano Perez",
                "nationality": "España",
                "birthdate": "2025-04-21",
                "family": self.family.id,
            },
            HTTP_AUTHORIZATION=f"Token {self.token4.key}",  # Pasar el token como encabezado de autorización
        )

        # Verificar si la solicitud fue exitosa (status code 201)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_student(self):
        student = Student.objects.create(
            name="Amadeo",
            surname="Portillo",
            education_center=self.education,
            is_morning_student=True,
            activities_during_exit="",
            status="RECHAZADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Carlos Perez",
            nationality="Alemania",
            birthdate="2015-04-21",
            family=self.family,
        )

        # Autenticar la solicitud GET con el token de autenticación
        response = self.client.get(
            f"/api/student/{student.id}/", HTTP_AUTHORIZATION=f"Token {self.token4.key}"
        )
        # Verificar que la solicitud fue exitosa (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificar que los datos del estudiante devueltos sean correctos
        self.assertEqual(response.data["name"], "Amadeo")
        self.assertEqual(response.data["surname"], "Portillo")


    def test_update_student(self):
        student = Student.objects.create(
            name="Alicia",
            surname="Jurado Ruz",
            education_center=self.education,
            is_morning_student=True,
            activities_during_exit="",
            status="PENDIENTE",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Carlos Perez",
            nationality="España",
            birthdate="2017-04-21",
            family=self.family,
        )

        # Authenticate the PUT request with the authentication token
        response = self.client.put(
            f"/api/student/{student.id}/",
            data={
                "name": "Alicia",
                "surname": "Jurado Ruz",
                "education_center": self.education.id,
                "is_morning_student": True,
                "activities_during_exit": "",
                "status": "PENDIENTE",
                "current_education_year": "TRES AÑOS",
                "education_center_tutor": "Don José Perez",
                "nationality": "España",
                "birthdate": "2017-04-21",
                "family": self.family.id,
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token4.key}",
        )
        # Verify that the request was successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

   

    def test_update_student_name_error(self):
        student = Student.objects.create(
            name="Jaime",
            surname="José Ruz",
            education_center=self.education,
            is_morning_student=True,
            activities_during_exit="",
            status="ACEPTADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Carlos Perez",
            nationality="España",
            birthdate="2017-04-21",
            family=self.family,
        )

        # Authenticate the PUT request with the authentication token
        response = self.client.put(
            f"/api/student/{student.id}/",
            data={
                "name": "",
                "surname": "Jurado Ruz",
                "education_center": self.education.id,
                "is_morning_student": True,
                "activities_during_exit": "",
                "status": "ACEPTADO",
                "current_education_year": "TRES AÑOS",
                "education_center_tutor": "Don Manuel Perez",
                "nationality": "España",
                "birthdate": "2017-04-21",
                "family": self.family.id,
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token4.key}",
        )
        # Verify that the request was successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_student_surname_error(self):
        student = Student.objects.create(
            name="Arturo",
            surname="Miguel Ruz",
            education_center=self.education,
            is_morning_student=True,
            activities_during_exit="",
            status="RECHAZADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Miguel Perez",
            nationality="España",
            birthdate="2017-04-21",
            family=self.family,
        )

        # Authenticate the PUT request with the authentication token
        response = self.client.put(
            f"/api/student/{student.id}/",
            data={
                "name": "Arturo",
                "surname": "",
                "education_center": self.education.id,
                "is_morning_student": True,
                "activities_during_exit": "",
                "status": "PENDIENTE",
                "current_education_year": "TRES AÑOS",
                "education_center_tutor": "Don José Perez",
                "nationality": "España",
                "birthdate": "2017-04-21",
                "family": self.family.id,
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token4.key}",
        )
        # Verify that the request was successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_student_birthday_error(self):
        student = Student.objects.create(
            name="Jorge",
            surname="Miguel Ruz",
            education_center=self.education,
            is_morning_student=False,
            activities_during_exit="",
            status="RECHAZADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Miguel Perez",
            nationality="México",
            birthdate="2017-04-21",
            family=self.family,
        )

        # Authenticate the PUT request with the authentication token
        response = self.client.put(
            f"/api/student/{student.id}/",
            data={
                "name": "Arturo",
                "surname": "",
                "education_center": self.education.id,
                "is_morning_student": True,
                "activities_during_exit": "",
                "status": "PENDIENTE",
                "current_education_year": "TRES AÑOS",
                "education_center_tutor": "Don José Perez",
                "nationality": "España",
                "birthdate": "2027-04-21",
                "family": self.family.id,
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token4.key}",
        )
        # Verify that the request was successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_student(self):
        student = Student.objects.create(**self.student_data)
        response = self.client.delete(
            f"/api/student/{student.id}/", HTTP_AUTHORIZATION=f"Token {self.token4.key}"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)


class QuaterMarkApiViewSetTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.educator = Educator.objects.create(birthdate="1989-04-21")
        self.education = EducationCenter.objects.create(name="San Francisco Asis")
        self.family = Family.objects.create(name="Familia Ruz")
        self.user = User.objects.create(
            username="testuser4",
            email="example4@gmail.com",
            role=FAMILY,
            family=self.family,
        )
        file_content = b"Test file content"
        self.marks = SimpleUploadedFile("marks.pdf", file_content)

        self.student = Student.objects.create(
            name="Pablo",
            surname="Castillo Priego",
            education_center=self.education,
            is_morning_student=True,
            activities_during_exit="",
            status="ACEPTADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Carlos Sainz",
            nationality="España",
            birthdate="2015-04-21",
            family=self.family,
        )

        # Crear un token de autenticación para el usuario
        self.token = Token.objects.create(user=self.user)

    def test_create_quaterMarks(self):
        quater = QuarterMarks.objects.count()
        response = self.client.post(
            "/api/quarter-marks/",
            data={
                "date": "2024-01-21",
                "marks": self.marks,
                "student": self.student.id,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        print(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(QuarterMarks.objects.count(), quater + 1)

    def test_obtain_quater_authorization(self):
        marks = QuarterMarks.objects.create(
            date="2023-01-21", marks=self.marks, student=self.student
        )
        response = self.client.get(
            f"/api/quarter-marks/{marks.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_quater_authorization_family(self):
        marks = QuarterMarks.objects.create(
            date="2023-06-21", marks=self.marks, student=self.student
        )
        response = self.client.delete(
            f"/api/quarter-marks/{marks.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 204)
