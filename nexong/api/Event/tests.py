from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory


class Event_ApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.family = Family.objects.create(name="Familia Pedraza")
        self.education_center = EducationCenter.objects.create(
            name="San Francisco Solano"
        )
        self.educator = Educator.objects.create(birthdate="2000-04-21")
        self.user = User.objects.create(
            username="usuariotest",
            email="usuariotets@gmail.com",
            role=FAMILY,
            family=self.family,
        )
        self.token = Token.objects.create(user=self.user)

        self.student = Student.objects.create(
            name="José Antonio",
            surname="Carmona",
            education_center=self.education_center,
            is_morning_student=False,
            activities_during_exit="",
            status="ACEPTADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Sebastian Perez",
            nationality="España",
            birthdate="2017-04-21",
            family=self.family,
        )
        self.student2 = Student.objects.create(
            name="Andrés",
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

        self.voluntario = Volunteer.objects.create(
            academic_formation="Test ",
            motivation="Test n",
            status="PENDIENTE",
            address="Test address2",
            postal_code=12350,
            birthdate="1956-07-05",
            start_date="1956-07-05",
            end_date="1956-07-05",
        )
        self.voluntario2 = Volunteer.objects.create(
            academic_formation="Test formation5",
            motivation="Test motivation4",
            status="ACEPTADO",
            address="Test address4",
            postal_code=12349,
            birthdate="1956-07-05",
            start_date="1956-07-05",
            end_date="1956-07-05",
        )

    def test_obtain_event_by_family(self):
        event = Event.objects.create(
            name="Vienen los lunnis",
            description="Se necesitan 3 voluntarios para hacer de Lucho",
            place="Jardín principal",
            max_volunteers=2,
            max_attendees=2,
            price=5,
            start_date="2024-06-12 06:00-00:00",
            end_date="2024-06-12 11:00-00:00",
        )
        event.attendees.add(self.student, self.student2)
        event.volunteers.add(self.voluntario, self.voluntario2)
        response = self.client.get(
            f"/api/event/{event.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_event(self):
        event1 = Event.objects.create(
            name="Vienen barrio Sesamo",
            description="Se necesitan voluntarios",
            place="Patio Principal",
            max_volunteers=2,
            max_attendees=2,
            price=5,
            start_date="2024-06-12 06:00-00:00",
            end_date="2024-06-12 11:00-00:00",
        )
        event1.attendees.add(self.student, self.student2)
        event1.volunteers.add(self.voluntario, self.voluntario2)

        # Obtener los IDs de los asistentes y voluntarios
        attendees_ids = [student.id for student in event1.attendees.all()]
        volunteers_ids = [volunteer.id for volunteer in event1.volunteers.all()]

        response = self.client.put(
            f"/api/event/{event1.id}/",
            data={
                "name": "Vienen Barrio Sesamo",
                "description": "Se necesitan voluntarios",
                "place": "Patio Principal",
                "max_volunteers": 2,
                "max_attendees": 2,
                "price": 5,
                "start_date": "2024-06-12 06:00-00:00",
                "end_date": "2024-06-12 11:00-00:00",
                "attendees": attendees_ids,  # Pasar IDs de los asistentes
                "volunteers": volunteers_ids,  # Pasar IDs de los voluntarios
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LessonEvent_ApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.family = Family.objects.create(name="Familia Bartolomé")
        self.education_center = EducationCenter.objects.create(name="San José")
        self.educator = Educator.objects.create(birthdate="2000-04-21")
        self.educator2 = Educator.objects.create(birthdate="2001-04-21")
        self.user = User.objects.create(
            username="testlessonevent",
            email="lessonevent2@gmail.com",
            role=FAMILY,
            family=self.family,
        )
        self.token = Token.objects.create(user=self.user)

        self.student = Student.objects.create(
            name="José David",
            surname="Garcia",
            education_center=self.education_center,
            is_morning_student=False,
            activities_during_exit="",
            status="ACEPTADO",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Sebastian Perez",
            nationality="Italia",
            birthdate="2019-04-21",
            family=self.family,
        )
        self.student2 = Student.objects.create(
            name="Andrés",
            surname="Caicedo",
            education_center=self.education_center,
            is_morning_student=True,
            activities_during_exit="",
            status="PENDIENTE",
            current_education_year="TRES AÑOS",
            education_center_tutor="Don Sebastian Perez",
            nationality="Colombia",
            birthdate="2015-04-21",
            family=self.family,
        )

        self.voluntario = Volunteer.objects.create(
            academic_formation="Test9 ",
            motivation="Test 56n",
            status="PENDIENTE",
            address="Test address289",
            postal_code=12350,
            birthdate="1956-07-05",
            start_date="1956-07-05",
            end_date="1959-07-05",
        )
        self.voluntario2 = Volunteer.objects.create(
            academic_formation="Test formation56",
            motivation="Test motivation89",
            status="ACEPTADO",
            address="Test addres56",
            postal_code=12349,
            birthdate="1956-07-05",
            start_date="1956-07-05",
            end_date="1958-07-05",
        )
        self.lesson = Lesson.objects.create(
            name="PRIMER CICLO 2",
            description="Módulo VI, segunda planta",
            capacity=4,
            is_morning_lesson=False,
            educator=self.educator,
            start_date="2024-01-28",
            end_date="2024-05-28",
        )

    def test_obtain_lesson_event_by_family(self):
        lessonevent = LessonEvent.objects.create(
            name="Vienen los Vengadores",
            description="Se necesitan 2 Vengadores",
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

    def test_update_lesson_event_error(self):
        lessonevent2 = LessonEvent.objects.create(
            name="Vienen la  Liga de la Justicia",
            description="Se necesitan 2 superheroes",
            place="Jardín principal",
            max_volunteers=2,
            lesson=self.lesson,
            price=6,
            start_date="2024-06-12 06:00-00:00",
            end_date="2024-06-12 11:00-00:00",
        )
        lessonevent2.attendees.add(self.student, self.student2)
        lessonevent2.volunteers.add(self.voluntario, self.voluntario2)
        lessonevent2.educators.add(self.educator, self.educator2)

        # Obtener los IDs de los asistentes y voluntarios
        attendees_ids = [student.id for student in lessonevent2.attendees.all()]
        volunteers_ids = [volunteer.id for volunteer in lessonevent2.volunteers.all()]
        educators_ids = [educator.id for educator in lessonevent2.educators.all()]

        response = self.client.put(
            f"/api/lesson-event/{lessonevent2.id}/",
            data={
                "name": "Vienen Barrio Sesamo",
                "description": "Se necesitan voluntarios",
                "place": "Patio Principal",
                "max_volunteers": 2,
                "price": 5,
                "lesson": self.lesson.id,
                "start_date": "2024-06-12 06:00-00:00",
                "end_date": "2024-06-12 11:00-00:00",
                "educators": educators_ids,
                "attendees": attendees_ids,
                "volunteers": volunteers_ids,
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminEventApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.family = Family.objects.create(name="Familia Ruz")
        self.education_center = EducationCenter.objects.create(
            name="San Francisco Asis"
        )
        self.educator = Educator.objects.create(
            description="testdeprueba4", birthdate="2002-04-21"
        )
        self.educator2 = Educator.objects.create(
            description="testdeprueba5", birthdate="2001-06-21"
        )
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
        volunteers_id1 = [
            self.voluntario.id,
            self.voluntario2.id,
        ]  # Asegurarse de que se esté pasando el ID del voluntario
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
        lessonevent2 = LessonEvent.objects.create(
            name="Vienen el Sevilla",
            description="Se necesitan 2 cantautores",
            place="Jardín principal",
            max_volunteers=2,
            lesson=self.lesson,
            price=5,
            start_date="2024-06-13 05:00-00:00",
            end_date="2024-06-13 11:00-00:00",
        )
        lessonevent2.attendees.add(self.student, self.student2)
        lessonevent2.volunteers.add(self.voluntario, self.voluntario2)
        lessonevent2.educators.add(self.educator, self.educator2)
        response = self.client.get(
            f"/api/lesson-event/{lessonevent2.id}/",
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


class VolunteerEventApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.volunteer = Volunteer.objects.create(
            id=1,
            academic_formation="Test formation",
            motivation="Test motivation",
            status="ACEPTADO",
            address="Test address",
            postal_code="12345",
            birthdate="1956-07-05",
            start_date="1956-07-05",
        )
        self.volunteer2 = Volunteer.objects.create(
            id=2,
            academic_formation="Test formation2",
            motivation="Test motivation2",
            status="ACEPTADO",
            address="Test address2",
            postal_code="12345",
            birthdate="1956-07-05",
            start_date="1956-07-05",
        )
        self.educator = Educator.objects.create(
            description="testdepruebaPas", birthdate="2000-04-21"
        )
        self.user2 = User.objects.create(
            username="usuariotest",
            email="usuariotets@gmail.com",
            role=VOLUNTEER,
            volunteer=self.volunteer,
        )

        self.token = Token.objects.create(user=self.user2)
        self.lesson = Lesson.objects.create(
            name="Ciclas",
            description="Módulo 2",
            capacity=16,
            is_morning_lesson=False,
            educator=self.educator,
            start_date="2024-01-26",
            end_date="2024-05-28",
        )

        self.event2 = Event.objects.create(
            name="Feria",
            description="Se necesitan 2 camareros para atenderlas",
            place="Cacharritos1",
            max_volunteers=2,
            max_attendees=2,
            price=5,
            start_date="2024-06-13 06:00-00:00",
            end_date="2024-06-13 11:00-00:00",
        )
        self.lessonevent2 = LessonEvent.objects.create(
            name="Vienen los del Ríopol",
            description="Se necesitan educadoresad",
            place="Patio Centrales",
            max_volunteers=3,
            price=25.0,
            lesson=self.lesson,
            start_date="2025-06-13T05:00:00Z",
            end_date="2025-06-13T16:00:00Z",
        )

    def test_obtain_event_by_volunteer(self):
        response = self.client.get(
            f"/api/event/{self.event2.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_event_by_volunteer_errpr(self):
        response = self.client.post(
            "/api/event/",
            data={
                "name": "Viene la familia Peruana",
                "description": "Se necesitan gente",
                "place": "La cocina",
                "max_volunteers": 2,
                "max_attendees": 2,
                "price": 5,
                "start_date": "2025-06-12T06:00:00Z",
                "end_date": "2025-06-12T11:00:00Z",
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_event_by_volunteer(self):
        volunteers_ids = [1,2]
        attendees_ids = list(self.event2.attendees.values_list('id', flat=True))
        response = self.client.put(
            f"/api/event/{self.event2.id}/",
            data={
                "name": self.event2.name,
                "description": self.event2.description,
                "place": self.event2.place,
                "max_volunteers": self.event2.max_volunteers,
                "max_attendees": self.event2.max_attendees,
                "price": self.event2.price,
                "start_date": self.event2.start_date,
                "end_date": self.event2.end_date,
                "volunteers": volunteers_ids,  # Pass the volunteer IDs in the request data
                "attendees": attendees_ids,
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtain_lesson_event_by_volunteer(self):
        lessonevent = LessonEvent.objects.create(
            name="Feriaa",
            description="Necesitamos camareros",
            place="Fuera",
            max_volunteers=2,
            lesson=self.lesson,
            price=5,
            start_date="2024-06-12 06:00-00:00",
            end_date="2024-07-12 11:00-00:00",
        )
        response = self.client.get(
            f"/api/lesson-event/{lessonevent.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_lesson_event_by_volunteer(self):
        volunteers_ids = [1, 2]
        data = {
            "name": self.lessonevent2.name,
            "description": self.lessonevent2.description,
            "place": self.lessonevent2.place,
            "max_volunteers": self.lessonevent2.max_volunteers,
            "price": self.lessonevent2.price,
            "lesson": self.lessonevent2.lesson.id,
            "start_date": self.lessonevent2.start_date,
            "end_date": self.lessonevent2.end_date,
            "volunteers": volunteers_ids,  # Pass the volunteer IDs in the request data
        }
        response = self.client.put(
            f"/api/lesson-event/{self.lessonevent2.id}/",
            data=data,  # Updating volunteers field
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lessonevent2.refresh_from_db()
