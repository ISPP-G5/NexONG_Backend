from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    URLValidator,
)


ADMIN = "ADMIN"
EDUCATOR = "EDUCATOR"
VOLUNTEER = "VOLUNTEER"
FAMILY = "FAMILY"
PARTNER = "PARTNER"
VOLUNTEER_PARTNER = "VOLUNTEER_PARTNER"
ROLE = [
    (ADMIN, "Administrador"),
    (VOLUNTEER, "Voluntario"),
    (EDUCATOR, "Educador"),
    (FAMILY, "Familia"),
    (PARTNER, "Socio"),
    (VOLUNTEER_PARTNER, "Voluntario y socio"),
]
PENDING = "PENDING"
ACCEPTED = "ACCEPTED"
REJECTED = "REJECTED"
EXPIRED = "EXPIRED"
STATUS = [
    (PENDING, "Pendiente"),
    (ACCEPTED, "Aceptado"),
    (REJECTED, "Rechazado"),
    (EXPIRED, "Caducado"),
]
ANNUAL = "ANNUAL"
MONTHLY = "MONTHLY"
QUARTERLY = "QUARTERLY"
SIXMONTHLY = "SIX-MONTHLY"
FREQUENCY = [
    (ANNUAL, "Anual"),
    (MONTHLY, "Mensual"),
    (QUARTERLY, "Trimestral"),
    (SIXMONTHLY, "Seis Meses"),
]
THREE_YEARS = "THREE_YEARS"
FOUR_YEARS = "FOUR_YEARS"
FIVE_YEARS = "FIVE_YEARS"
FIRST_PRIMARY = "FIRST_PRIMARY"
SECOND_PRIMARY = "SECOND_PRIMARY"
THIRD_PRIMARY = "THIRD_PRIMARY"
FOURTH_PRIMARY = "FOURTH_PRIMARY"
FIFTH_PRIMARY = "FIFTH_PRIMARY"
SIXTH_PRIMARY = "SIXTH_PRIMARY"
FIRST_SECONDARY = "FIRST_SECONDARY"
SECOND_SECONDARY = "SECOND_SECONDARY"
THIRD_SECONDARY = "THIRD_SECONDARY"
FOURTH_SECONDARY = "FOURTH_SECONDARY"
CURRENT_EDUCATION_YEAR = [
    (THREE_YEARS, "Tres años"),
    (FOUR_YEARS, "Cuatro años"),
    (FIVE_YEARS, "Cinco años"),
    (FIRST_PRIMARY, "Primero de primaria"),
    (SECOND_PRIMARY, "Segundo de primaria"),
    (THIRD_PRIMARY, "Tercero de primaria"),
    (FOURTH_PRIMARY, "Cuarto de primaria"),
    (FIFTH_PRIMARY, "Quinto de primaria"),
    (SIXTH_PRIMARY, "Sexto de primaria"),
    (FIRST_SECONDARY, "Primero de secundaria"),
    (SECOND_SECONDARY, "Segundo de secundaria"),
    (THIRD_SECONDARY, "Tercero de secundaria"),
    (FOURTH_SECONDARY, "Cuarto de secundaria"),
]

ZERO_TO_ONE = "ZERO_TO_ONE"
ONE_TO_FIVE = "ONE_TO_FIVE"
ZERO_TO_TEN = "ZERO_TO_TEN"
GRADESYSTEM = [
    (ZERO_TO_ONE, "0-1"),
    (ONE_TO_FIVE, "1-5"),
    (ZERO_TO_TEN, "0-10"),
]
DAILY = "DAILY"
ANNUAL = "ANNUAL"
EVALUATION_TYPE = [
    (DAILY, "Diario"),
    (ANNUAL, "Anual"),
]
WEEKDAYS = [
    ("MONDAY", "Lunes"),
    ("TUESDAY", "Martes"),
    ("WEDNESDAY", "Miércoles"),
    ("THURSDAY", "Jueves"),
    ("FRIDAY", "Viernes"),
    ("SATURDAY", "Sábado"),
    ("SUNDAY", "Domingo"),
]


class Family(models.Model):
    name = models.CharField(max_length=255)


class EducationCenter(models.Model):
    name = models.CharField(max_length=255)


class Student(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    current_education_year = models.CharField(
        max_length=20, choices=CURRENT_EDUCATION_YEAR, default=THREE_YEARS
    )
    education_center_tutor = models.CharField(max_length=255)
    enrollment_document = models.FileField(
        upload_to="files/student_enrollment", null=True, blank=True
    )
    scanned_sanitary_card = models.FileField(
        upload_to="files/student_sanitary", null=True, blank=True
    )
    nationality = models.CharField(max_length=255)
    birthdate = models.DateField()
    is_morning_student = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING, null=True)
    activities_during_exit = models.CharField(max_length=1000, null=True, blank=True)
    education_center = models.ForeignKey(
        EducationCenter,
        on_delete=models.CASCADE,
        related_name="education_center",
        null=True,
        blank=True,
    )
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, related_name="students", null=True, blank=True
    )


class QuarterMarks(models.Model):
    date = models.DateField()
    marks = models.FileField(upload_to="files/quarter_marks")
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="quarter_marks"
    )


class Partner(models.Model):
    address = models.CharField(max_length=255, null=True, blank=True)
    enrollment_document = models.FileField(upload_to="files/partner_enrollment")
    birthdate = models.DateField(null=True)


class Donation(models.Model):
    iban = models.CharField(max_length=34, unique=True)
    quantity = models.DecimalField(
        default=Decimal("0.01"),
        validators=[MinValueValidator(Decimal("0.01"))],
        max_digits=10,
        decimal_places=2,
    )
    frequency = models.CharField(max_length=11, choices=FREQUENCY, default=MONTHLY)
    holder = models.CharField(max_length=255)
    quota_extension_document = models.FileField(
        null=True, blank=True, upload_to="files/partner_quota"
    )
    date = models.DateField()
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name="donations"
    )


class Volunteer(models.Model):
    academic_formation = models.CharField(max_length=1000)
    motivation = models.CharField(max_length=1000)
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING)
    address = models.CharField(max_length=255)
    postal_code = models.IntegerField(
        validators=[MinValueValidator(00000), MaxValueValidator(90000)], default=10000
    )
    enrollment_document = models.FileField(upload_to="files/volunteer_enrollment")
    registry_sheet = models.FileField(upload_to="files/volunteer_registry")
    sexual_offenses_document = models.FileField(upload_to="files/volunteer_offenses")
    scanned_id = models.FileField(upload_to="files/volunteer_id")
    minor_authorization = models.FileField(
        null=True, blank=True, upload_to="files/volunteer_minor"
    )
    scanned_authorizer_id = models.FileField(
        null=True, blank=True, upload_to="files/volunteer_authorizer_id"
    )
    birthdate = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class Educator(models.Model):
    birthdate = models.DateField(null=True)


class User(AbstractBaseUser):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=100)
    id_number = models.CharField(max_length=9, unique=True)
    phone = models.IntegerField(
        validators=[MaxValueValidator(999999999), MinValueValidator(600000000)],
        blank=True,
        null=True,
    )
    password = models.CharField(
        max_length=100
    )  # Antes de guardar en la db, se debe hacer user.set_password(password)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=25,
        choices=ROLE,
        default=FAMILY,
    )
    avatar = models.URLField(blank=True, null=True, validators=[URLValidator()])
    family = models.OneToOneField(
        Family, on_delete=models.CASCADE, blank=True, null=True
    )
    partner = models.OneToOneField(
        Partner, on_delete=models.CASCADE, blank=True, null=True
    )
    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, blank=True, null=True
    )
    education_center = models.OneToOneField(
        EducationCenter, on_delete=models.CASCADE, blank=True, null=True
    )
    educator = models.OneToOneField(
        Educator, on_delete=models.CASCADE, blank=True, null=True
    )

    USERNAME_FIELD = "email"


class Meeting(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date = models.DateField(blank=True)
    time = models.DateTimeField(blank=True)
    attendees = models.ManyToManyField(Partner, related_name="meetings_attending")


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    capacity = models.IntegerField(validators=[MinValueValidator(0)], blank=True)
    is_morning_lesson = models.BooleanField(default=True)
    educator = models.ForeignKey(
        Educator, on_delete=models.CASCADE, related_name="lessons"
    )
    students = models.ManyToManyField(
        Student, related_name="lessons", blank=True, null=True
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Schedule(models.Model):
    weekday = models.CharField(max_length=10, choices=WEEKDAYS, default="MONDAY")
    start_time = models.TimeField()
    end_time = models.TimeField()
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="schedules"
    )


class EvaluationType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    evaluation_type = models.CharField(
        max_length=10, choices=EVALUATION_TYPE, default=DAILY
    )
    grade_system = models.CharField(
        max_length=20, choices=GRADESYSTEM, default=ZERO_TO_TEN
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="student_evaluations"
    )


class StudentEvaluation(models.Model):
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], default=0
    )
    date = models.DateField()
    comment = models.CharField(max_length=1000, null=True, blank=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student_evaluations"
    )
    evaluation_type = models.ForeignKey(
        EvaluationType, on_delete=models.CASCADE, related_name="student_evaluations"
    )


class LessonAttendance(models.Model):
    date = models.DateField()
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="lesson_attendances"
    )
    volunteer = models.ForeignKey(
        Volunteer, on_delete=models.CASCADE, related_name="lesson_attendances"
    )


class LessonEvent(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    place = models.CharField(max_length=1000)
    max_volunteers = models.IntegerField(validators=[MinValueValidator(0)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    educators = models.ManyToManyField(Educator, related_name="lesson_events")
    attendees = models.ManyToManyField(
        Student, related_name="lesson_events", null=True, blank=True
    )
    volunteers = models.ManyToManyField(
        Volunteer, related_name="lesson_events", null=True, blank=True
    )


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    place = models.CharField(max_length=1000)
    max_volunteers = models.IntegerField(validators=[MinValueValidator(0)])
    max_attendees = models.IntegerField(validators=[MinValueValidator(0)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    attendees = models.ManyToManyField(
        Student, related_name="events", null=True, blank=True
    )
    volunteers = models.ManyToManyField(Volunteer, related_name="events")


class CenterExitAuthorization(models.Model):
    authorization = models.FileField(upload_to="files/centerexit_auth")
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="center_exits"
    )
    is_authorized = models.BooleanField(default=False)
    lesson_event = models.ForeignKey(
        LessonEvent, on_delete=models.CASCADE, related_name="center_exit_authorizations"
    )
