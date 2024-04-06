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
            username="testuser2",
            email="example2@gmail.com",
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
            name = "Vienen los lunnis",
            description =  "Se necesitan 3 voluntarios para hacer de Lucho",
            place =  "Jardín principal",
            max_volunteers =  2,
            max_attendees =  2,
            price =  5,
            start_date = "2024-06-12 06:00-00:00",
            end_date = "2024-06-12 11:00-00:00"
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
            end_date="2024-06-12 11:00-00:00"
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
                "volunteers": volunteers_ids  # Pasar IDs de los voluntarios
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LessonEvent_ApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.family = Family.objects.create(name="Familia Bartolomé")
        self.education_center = EducationCenter.objects.create(
            name="San José"
        )
        self.educator = Educator.objects.create(birthdate="2000-04-21")
        self.educator2 = Educator.objects.create(birthdate="2001-04-21")
        self.user = User.objects.create(
            username="testuser2",
            email="example2@gmail.com",
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
            name = "Vienen los Vengadores",
            description =  "Se necesitan 2 Vengadores",
            place =  "Jardín principal",
            max_volunteers =  2,
            lesson = self.lesson,
            price =  5,
            start_date = "2024-06-12 06:00-00:00",
            end_date = "2024-06-12 11:00-00:00"
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
            name = "Vienen la  Liga de la Justicia",
            description =  "Se necesitan 2 superheroes",
            place =  "Jardín principal",
            max_volunteers =  2,
            lesson = self.lesson,
            price =  6,
            start_date = "2024-06-12 06:00-00:00",
            end_date = "2024-06-12 11:00-00:00"
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
                "lesson" : self.lesson.id,
                "start_date": "2024-06-12 06:00-00:00",
                "end_date": "2024-06-12 11:00-00:00",
                "educators": educators_ids,
                "attendees": attendees_ids,  
                "volunteers": volunteers_ids  
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    

    