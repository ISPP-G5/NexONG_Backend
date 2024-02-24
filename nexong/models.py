from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    URLValidator,
)

# Create your models here.

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
STATUS = [
    (PENDING, "Pendiente"),
    (ACCEPTED, "Aceptado"),
    (REJECTED, "Rechazado"),
]
ANNUAL = "ANNUAL"
MENSUAL = "MENSUAL"
QUARTERLY = "QUARTERLY"
SIXMONTHLY = "SIX-MONTHLY"
FRECUENCY = [
    (ANNUAL, "Anual"),
    (MENSUAL, "Mensual"),
    (QUARTERLY, "Trimestral"),
    (SIXMONTHLY, " Seis Meses"),
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


class Family(models.Model):
    name = models.CharField(max_length=255)


class Student(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    education_center = models.CharField(max_length=255)
    current_education_year = models.CharField(
        max_length=20, choices=CURRENT_EDUCATION_YEAR, default=THREE_YEARS
    )
    education_center_tutor = models.CharField(max_length=255)
    enrollment_document = models.FileField()
    scanned_sanitary_card = models.FileField()
    nationality = models.CharField(max_length=255)
    birthdate = models.DateField()
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, related_name="students", null=True, blank=True
    )


class Partner(models.Model):
    holder = models.CharField(max_length=255)
    iban = models.CharField(max_length=34, unique=True)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    frequency = models.CharField(max_length=11, choices=FRECUENCY, default=MENSUAL)
    address = models.CharField(max_length=255, null=True, blank=True)
    enrollment_document = models.FileField()
    quota_extension_document = models.FileField(null=True, blank=True)
    birthdate = models.DateField(null=True)


class Volunteer(models.Model):
    academic_formation = models.CharField(max_length=1000)
    motivation = models.CharField(max_length=1000)
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING)
    address = models.CharField(max_length=255)
    postal_code = models.IntegerField(
        validators=[MinValueValidator(10000), MaxValueValidator(90000)], default=10000
    )
    enrollment_document = models.FileField()
    registry_sheet = models.FileField()
    sexual_offenses_document = models.FileField()
    scanned_id = models.FileField()
    minor_authorization = models.FileField(null=True, blank=True)
    scanned_authorizer_id = models.FileField(null=True, blank=True)
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
    educator = models.OneToOneField(
        Educator, on_delete=models.CASCADE, blank=True, null=True
    )
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"


class Meeting(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date = models.DateField(blank=True)
    time = models.DateTimeField(blank=True)
    attendees = models.ManyToManyField(Partner, related_name="meetings_attending")


class Comment(models.Model):
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments_made"
    )
    commentee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments_received"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    capacity = models.IntegerField(validators=[MinValueValidator(0)], blank=True)
    is_morning_lesson = models.BooleanField(default=True)
    educator = models.ForeignKey(
        Educator, on_delete=models.CASCADE, related_name="lessons"
    )
    students = models.ManyToManyField(Student, related_name="lessons")


class StudentEvaluation(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    grade_system = models.CharField(
        max_length=20, choices=GRADESYSTEM, default=ZERO_TO_TEN
    )
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], default=0
    )
    date = models.DateField()
    evaluation_type = models.CharField(
        max_length=10, choices=EVALUATION_TYPE, default=DAILY
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="student_evaluations"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="student_evaluations"
    )


class LessonEvaluation(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    grade_system = models.CharField(
        max_length=20, choices=GRADESYSTEM, default=ZERO_TO_TEN
    )
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], default=0
    )
    date = models.DateField()
    evaluation_type = models.CharField(
        max_length=10, choices=EVALUATION_TYPE, default=DAILY
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="lesson_evaluations"
    )
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, related_name="lesson_evaluations"
    )


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    place = models.CharField(max_length=1000)
    capacity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    max_volunteers = models.IntegerField(validators=[MinValueValidator(0)])
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    attendees = models.ManyToManyField(User, related_name="events")


class CenterExitAuthorization(models.Model):
    authorization = models.FileField()
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="center_exits"
    )
    is_authorized = models.BooleanField(default=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="center_exit_authorizations"
    )
