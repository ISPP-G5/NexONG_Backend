from django.core.files.uploadedfile import SimpleUploadedFile
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory


def testSetupEducator(self):
    self.factory = APIRequestFactory()
    self.educator_data = {
        "description": "Test description",
        "birthdate": "1969-06-09",
    }
    self.educator_error_desc = {
        "description": "",
        "birthdate": "1969-06-09",
    }
    self.educator_error_date = {
        "description": "Test description",
        "birthdate": "2069-06-09",
    }
    self.family = Family.objects.create(name="Los Morales del Valle")
    self.educator = Educator.objects.create(
        birthdate="1969-06-09", description="EL profesor de lengua de Manos abiertas"
    )
    self.user = User.objects.create(
        username="educatortestusernexong",
        email="educatorone@gmail.com",
        role=EDUCATOR,
        educator=self.educator,
    )
    self.token = Token.objects.create(user=self.user)
    self.educator2 = Educator.objects.create(birthdate="1969-03-21")
    self.educator3 = Educator.objects.create(birthdate="1987-05-22")
    self.education_center = EducationCenter.objects.create(name="Virgen de la Pureza")
    self.student = Student.objects.create(
        name="Luis",
        surname="Morales",
        education_center=self.education_center,
        is_morning_student=True,
        activities_during_exit="",
        status="ACEPTADO",
        current_education_year="CUATRO AÑOS",
        education_center_tutor="Don Joaquin Medina",
        nationality="Frances",
        birthdate="2015-04-21",
        family=self.family,
    )
    self.volunteer = Volunteer.objects.create(
        academic_formation="Test Volunteer for educator",
        motivation="volunteer motivation",
        status="ACEPTADO",
        address="Centro sevilla",
        postal_code=13334,
        birthdate="1976-07-05",
        start_date="2001-02-08",
        end_date="2008-07-09",
    )
    self.lesson = Lesson.objects.create(
        name="Lengua y literatura",
        description="Clases de lengua de segundo de ESO",
        capacity=20,
        is_morning_lesson=True,
        educator=self.educator,
        start_date="2025-01-28",
        end_date="2025-07-29",
    )
    self.lesson_event = LessonEvent.objects.create(
        name="Taller de manualidades",
        description="Taller para los niños con los voluntarios",
        place="Centro de Montequinto",
        price=5,
        max_volunteers=6,
        start_date="2025-04-18 17:00-00:00",
        end_date="2025-04-18 20:00-00:00",
        lesson=self.lesson,
    )
    self.center_exit = {
        "student": self.student,
        "is_authorized": True,
        "lesson_event": self.lesson_event,
    }
    file_content = b"test for center exit authorization"
    self.center_exit["authorization"] = SimpleUploadedFile(
        "ce_authorization.pdf", file_content
    )
    self.lesson_data = {
        "name": "Filosofia",
        "description": "Filosofia para los de cuarto de ESO",
        "capacity": 20,
        "is_morning_lesson": True,
        "educator": self.educator,
        "start_date": "2024-01-28",
        "end_date": "2024-07-28",
    }
    self.lessonAtendance_data = {
        "date": "2024-02-23",
        "lesson": self.lesson,
        "volunteer": self.volunteer,
    }
    self.quartermarks = {"date": "2024-03-05", "student": self.student}
    file_content = b"Test content for quartermarks"
    self.quartermarks["marks"] = SimpleUploadedFile("marks.pdf", file_content)
    self.student_data = {
        "name": "Guillermo",
        "surname": "Morales",
        "education_center": self.education_center,
        "is_morning_student": True,
        "activities_during_exit": "",
        "status": "ACEPTADO",
        "current_education_year": "CINCO AÑOS",
        "education_center_tutor": "Reina Victoria",
        "nationality": "Frances",
        "birthdate": "2014-04-21",
        "family": self.family,
    }
    self.lesson2 = Lesson.objects.create(
        name="Plastica",
        description="Manualidades para niños de cuatro años",
        capacity=15,
        is_morning_lesson=True,
        educator=self.educator2,
        start_date="2024-08-28",
        end_date="2024-09-28",
    )
    self.evaluation_type_data = {
        "name": "Asistencia",
        "description": "asitencia diaria",
        "evaluation_type": "DIARIO",
        "grade_system": "CERO A UNO",
        "lesson": self.lesson,
    }
    self.evaluation_type_data_forbiden = {
        "name": "Nota Lengua",
        "description": "Puntuacion del alumno en lengua y literatura",
        "evaluation_type": "ANUAL",
        "grade_system": "CERO A DIEZ",
        "lesson": self.lesson2,
    }
    self.evaluation_type_data_bad_request = {
        "name": "",
        "description": "Notas plastica",
        "evaluation_type": "TRIMESTRAL",
        "grade_system": "UNO A CINCO",
        "lesson": self.lesson,
    }
    self.evaluation_type = EvaluationType.objects.create(
        name="Asistencia",
        description="asitencia diaria",
        evaluation_type=DAILY,
        grade_system=ZERO_TO_ONE,
        lesson=self.lesson,
    )
    self.evaluation_type2 = EvaluationType.objects.create(
        name="Nota Lengua",
        description="Puntuacion del alumno en lengua y literatura",
        evaluation_type=ANNUAL,
        grade_system=ZERO_TO_TEN,
        lesson=self.lesson2,
    )
    self.student_eval_data = {
        "grade": 0,
        "date": "2024-01-28",
        "comment": "Puede mejorar",
        "student": self.student,
        "evaluation_type": self.evaluation_type,
    }
    self.student_eval_data_forbiden = {
        "grade": 5,
        "date": "2024-01-28",
        "comment": "Suficiente",
        "student": self.student,
        "evaluation_type": self.evaluation_type2,
    }
    self.student_eval_data_bad_request = {
        "grade": -1,
        "date": "2024-01-28",
        "comment": "No vino",
        "student": self.student,
        "evaluation_type": self.evaluation_type,
    }
    self.lesson.students.add(self.student)
    self.lesson2.students.add(self.student)
