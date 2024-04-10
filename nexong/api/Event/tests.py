from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token


class AdminEventApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.family = Family.objects.create(name="Familia Pedraza")
        self.education_center = EducationCenter.objects.create(
            name="San Francisco Solano"
        )
        self.educator = Educator.objects.create(birthdate="2000-04-21")
        self.educator2 = Educator.objects.create(birthdate="2001-06-21")
        self.user = User.objects.create(
            username="usuariotest",
            email="usuariotets@gmail.com",
            role=ADMIN,
        )
        self.token = Token.objects.create(user=self.user)

        self.student = Student.objects.create(
            name="José Manuel",
            surname="Colina",
            education_center=self.education_center,
            is_morning_student=False,
            activities_during_exit="",
            status="PENDIENTE",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Sebastian Perez",
            nationality="Colombia",
            birthdate="2017-04-21",
            family=self.family,
        )
        self.student2 = Student.objects.create(
            name="Jesulin",
            surname="Montes",
            education_center=self.education_center,
            is_morning_student=True,
            activities_during_exit="",
            status="PENDIENTE",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Amador Perez",
            nationality="España",
            birthdate="2015-04-21",
            family=self.family,
        )

        self.voluntario = Volunteer.objects.create(
            academic_formation="Test admin",
            motivation="Test adminn",
            status="PENDIENTE",
            address="Test address2",
            postal_code=12350,
            birthdate="1956-07-05",
            start_date="1956-07-05",
            end_date="1956-07-05",
        )
        self.voluntario2 = Volunteer.objects.create(
            academic_formation="Test formation6",
            motivation="Test motivation6",
            status="ACEPTADO",
            address="Test address4",
            postal_code=12349,
            birthdate="1956-07-05",
            start_date="1956-07-05",
            end_date="1956-07-05",
        )

        self.lesson = Lesson.objects.create(
            name="Ciclo Cocina",
            description="Módulo XV, cuarta planta",
            capacity=16,
            is_morning_lesson=False,
            educator=self.educator,
            start_date="2024-01-26",
            end_date="2024-05-28",
        )
        self.lesson.students.add(self.student, self.student2)

        self.event = Event.objects.create(
            name="Vienen el Córdoba",
            description="Se necesitan 2 voluntarios para atenderlos",
            place="Jardín exterior",
            max_volunteers=2,
            max_attendees=2,
            price=5,
            start_date="2024-06-13 06:00-00:00",
            end_date="2024-06-13 11:00-00:00",
        )
        self.event.attendees.add(self.student, self.student2)
        self.event.volunteers.add(self.voluntario, self.voluntario2)
        self.lesson2 = Lesson.objects.create(
            name="Ciclo Mecánica",
            description="Módulo XXIII, 3 planta",
            capacity=20,
            is_morning_lesson=False,
            educator=self.educator2,
            start_date="2024-01-26",
            end_date="2024-05-28",
        )

        self.lessonevent = LessonEvent.objects.create(
            name="Vienen los del Ríopol",
            description="Se necesitan educadoresad",
            place="Patio Centrales",
            max_volunteers=2,
            price=25.0,
            lesson=self.lesson,
            start_date="2025-06-13T05:00:00Z",
            end_date="2025-06-13T16:00:00Z",
        )

    def test_obtain_event_by_admin(self):
        response = self.client.get(
            f"/api/event/{self.event.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_event_by_admin(self):
        attendees_ids1 = [self.student.id, self.student2.id]
        volunteers_ids1 = [
            self.voluntario.id,
            self.voluntario2.id,
        ]  # Asegurarse de que se esté pasando el ID del voluntario
        response = self.client.post(
            "/api/event/",
            data={
                "name": "Viene la familia",
                "description": "Se necesitan gente",
                "place": "Patio Trasero",
                "max_volunteers": 2,
                "max_attendees": 2,
                "price": 5,
                "start_date": "2025-06-12T06:00:00Z",
                "end_date": "2025-06-12T11:00:00Z",
                "attendees": attendees_ids1,
                "volunteers": volunteers_ids1,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_date_past_error_by_admin(self):
        attendees_ids2 = [self.student.id, self.student2.id]
        volunteers_ids2 = [
            self.voluntario.id,
            self.voluntario2.id,
        ]  # Asegurarse de que se esté pasando el ID del voluntario
        response = self.client.post(
            "/api/event/",
            data={
                "name": "Vienen Barrio Sesamo",
                "description": "Se necesitan voluntarios",
                "place": "Patio Principal",
                "max_volunteers": 2,
                "max_attendees": 2,
                "price": 5,
                "start_date": "2023-06-12T06:00:00Z",
                "end_date": "2023-06-12T11:00:00Z",
                "attendees": attendees_ids2,
                "volunteers": volunteers_ids2,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_event_date_start_error_by_admin(self):
        attendees_ids3 = [self.student.id, self.student2.id]
        volunteers_ids3 = [
            self.voluntario.id,
            self.voluntario2.id,
        ]  # Asegurarse de que se esté pasando el ID del voluntario
        response = self.client.post(
            "/api/event/",
            data={
                "name": "Vienen Barrio Sesamo 45",
                "description": "Se necesitan voluntarios 56",
                "place": "Patio Secundario",
                "max_volunteers": 2,
                "max_attendees": 2,
                "price": 5,
                "start_date": "2023-06-13T06:00:00Z",
                "end_date": "2023-06-12T11:00:00Z",
                "attendees": attendees_ids3,
                "volunteers": volunteers_ids3,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_event_hour_start_error_by_admin(self):
        attendees_id1 = [self.student.id, self.student2.id]
        volunteers_id1 = [self.voluntario.id, self.voluntario2.id]  # Asegurarse de que se esté pasando el ID del voluntario
        response = self.client.post(
            "/api/event/",
            data={
                "name": "Vienen Barrio 65",
                "description": "Se necesitan voluntarios",
                "place": "Patio Trasesp",
                "max_volunteers": 2,
                "max_attendees": 2,
                "price": 5,
                "start_date": "2023-06-13T05:00:00Z",  
                "end_date": "2023-06-13T04:00:00Z",    
                "attendees": attendees_id1,
                "volunteers": volunteers_id1, 
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_lesson_event_by_admin(self):
        lessonevent = LessonEvent.objects.create(
            name="Vienen el Sevilla",
            description="Se necesitan 2 cantautores",
            place="Jardín principal",
            max_volunteers=2,
            lesson=self.lesson,
            price=5,
            start_date="2024-06-12 06:00-00:00",
            end_date="2024-06-12 11:00-00:00",
        )
        lessonevent.attendees.add(self.student, self.student2)
        lessonevent.volunteers.add(self.voluntario, self.voluntario2)
        lessonevent.educators.add(self.educator, self.educator2)
        response = self.client.get(
            f"/api/lesson-event/{lessonevent.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_event_by_admin(self):
        response = self.client.delete(
            f"/api/event/{self.event.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_lesson_event_by_admin(self):
        attendees_id2 = [self.student.id, self.student2.id]
        volunteers_id2 = [self.voluntario.id, self.voluntario2.id]  
        educators_id2 = [self.educator.id, self.educator2.id]
        response = self.client.post(
            "/api/lesson-event/",
            data={
                "name": "Vienen los Universitarios",
                "description": "Se necesitan gente",
                "place": "Patio Delantero",
                "max_volunteers": 2,
                "price": 26.0,
                "lesson": self.lesson.id,
                "start_date": "2025-06-13T05:00:00Z",  
                "end_date": "2025-06-13T16:00:00Z", 
                "educators": educators_id2,
                "attendees": attendees_id2,
                "volunteers": volunteers_id2,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_event_lesson_error_by_admin(self):
        attendees_id3 = [self.student.id, self.student2.id]
        volunteers_id3 = [self.voluntario.id, self.voluntario2.id]  
        educators_id3 = [self.educator.id, self.educator2.id]
        response = self.client.post(
            "/api/lesson-event/",
            data={
                "name": "Vienen los del Río",
                "description": "Se necesitan educadores",
                "place": "Patio Central",
                "max_volunteers": 2,
                "price": 25.0,
                "lesson": self.lesson2.id,
                "start_date": "2025-06-13T05:00:00Z",  
                "end_date": "2025-06-13T16:00:00Z", 
                "educators": educators_id3,
                "attendees": attendees_id3,
                "volunteers": volunteers_id3,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_lesson_event_date_error_by_admin(self):
        attendees_id4 = [self.student.id, self.student2.id]
        volunteers_id4 = [self.voluntario.id, self.voluntario2.id]  
        educators_id4 = [self.educator.id, self.educator2.id]
        response = self.client.post(
            "/api/lesson-event/",
            data={
                "name": "Vienen los del Río23",
                "description": "Se necesitan educadores25",
                "place": "Patio Central85",
                "max_volunteers": 2,
                "price": 25.0,
                "lesson": self.lesson.id,
                "start_date": "2023-06-13T05:00:00Z",  
                "end_date": "2023-06-13T16:00:00Z", 
                "educators": educators_id4,
                "attendees": attendees_id4,
                "volunteers": volunteers_id4,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_lesson_event_start_date_error_by_admin(self):
        attendees_id5 = [self.student.id, self.student2.id]
        volunteers_id5 = [self.voluntario.id, self.voluntario2.id]  
        educators_id5 = [self.educator.id, self.educator2.id]
        response = self.client.post(
            "/api/lesson-event/",
            data={
                "name": "Vienen los del Río78",
                "description": "Se necesitan educadorespo",
                "place": "Patio Centralaq",
                "max_volunteers": 2,
                "price": 30.0,
                "lesson": self.lesson2.id,
                "start_date": "2025-06-14T05:00:00Z",  
                "end_date": "2025-06-13T16:00:00Z", 
                "educators": educators_id5,
                "attendees": attendees_id5,
                "volunteers": volunteers_id5,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_lesson_event_start_hour_error_by_admin(self):
        attendees_id6 = [self.student.id, self.student2.id]
        volunteers_id6 = [self.voluntario.id, self.voluntario2.id]  
        educators_id6 = [self.educator.id, self.educator2.id]
        response = self.client.post(
            "/api/lesson-event/",
            data={
                "name": "Vienen los del Río780",
                "description": "Se necesitan educadorespos",
                "place": "Patio Centralaq",
                "max_volunteers": 2,
                "price": 21.0,
                "lesson": self.lesson2.id,
                "start_date": "2025-06-13T05:00:00Z",  
                "end_date": "2025-06-13T04:00:00Z", 
                "educators": educators_id6,
                "attendees": attendees_id6,
                "volunteers": volunteers_id6,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_lesson_event_by_admin(self):
        response = self.client.delete(
            f"/api/lesson-event/{self.lessonevent.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
