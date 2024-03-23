from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    URLValidator,
)
from nexong.api.helpers.fileValidations import (
    upload_to_authorization,
    upload_to_avatar,
    upload_to_education_center_tutor,
    upload_to_enrollment_document,
    upload_to_minor_authorization,
    upload_to_partner,
    upload_to_punctual_donation,
    upload_to_quota_extension_document,
    upload_to_quartermarks,
    upload_to_registry_sheet,
    upload_to_scanned_authorizer_id,
    upload_to_scanned_id,
    upload_to_scanned_sanitary_card,
    upload_to_sexual_offenses,
    validate_file_extension,
    validate_image_extension,
)

ADMIN = "ADMIN"
EDUCATOR = "EDUCADOR"
VOLUNTEER = "VOLUNTARIO"
FAMILY = "FAMILIA"
PARTNER = "SOCIO"
VOLUNTEER_PARTNER = "VOLUNTARIO_SOCIO"
EDUCATION_CENTER = "CENTRO EDUCATIVO"
ROLE = [
    (ADMIN, "Administrador"),
    (VOLUNTEER, "Voluntario"),
    (EDUCATOR, "Educador"),
    (FAMILY, "Familia"),
    (PARTNER, "Socio"),
    (VOLUNTEER_PARTNER, "Voluntario y socio"),
    (EDUCATION_CENTER, "Centro educativo"),
]
PENDING = "PENDIENTE"
ACCEPTED = "ACEPTADO"
REJECTED = "RECHAZADO"
EXPIRED = "CADUCADO"
STATUS = [
    (PENDING, "Pendiente"),
    (ACCEPTED, "Aceptado"),
    (REJECTED, "Rechazado"),
    (EXPIRED, "Caducado"),
]
ANNUAL = "ANUAL"
MONTHLY = "MENSUAL"
QUARTERLY = "TRIMESTRAL"
SIXMONTHLY = "SEMESTRAL"
FREQUENCY = [
    (ANNUAL, "Anual"),
    (MONTHLY, "Mensual"),
    (QUARTERLY, "Trimestral"),
    (SIXMONTHLY, "Seis Meses"),
]
THREE_YEARS = "TRES AÑOS"
FOUR_YEARS = "CUATRO AÑOS"
FIVE_YEARS = "CINCO AÑOS"
FIRST_PRIMARY = "PRIMERO PRIMARIA"
SECOND_PRIMARY = "SEGUNDO PRIMARIA"
THIRD_PRIMARY = "TERCERO PRIMARIA"
FOURTH_PRIMARY = "CUARTO PRIMARIA"
FIFTH_PRIMARY = "QUINTO PRIMARIA"
SIXTH_PRIMARY = "SEXTO PRIMARIA"
FIRST_SECONDARY = "PRIMERO SECUNDARIA"
SECOND_SECONDARY = "SEGUNDO SECUNDARIA"
THIRD_SECONDARY = "TERCERO SECUNDARIA"
FOURTH_SECONDARY = "CUARTO SECUNDARIA"
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

ZERO_TO_ONE = "CERO A UNO"
ONE_TO_FIVE = "UNO A CINCO"
ZERO_TO_TEN = "CERO A DIEZ"
GRADESYSTEM = [
    (ZERO_TO_ONE, "0-1"),
    (ONE_TO_FIVE, "1-5"),
    (ZERO_TO_TEN, "0-10"),
]
DAILY = "DIARIO"
ANNUAL = "ANUAL"
EVALUATION_TYPE = [
    (DAILY, "Diario"),
    (ANNUAL, "Anual"),
]
WEEKDAYS = [
    ("LUNES", "Lunes"),
    ("MARTES", "Martes"),
    ("MIERCOLES", "Miércoles"),
    ("JUEVES", "Jueves"),
    ("VIERNES", "Viernes"),
    ("SABADO", "Sábado"),
    ("DOMINGO", "Domingo"),
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
        upload_to=upload_to_education_center_tutor,
        null=True,
        blank=True,
        validators=[validate_file_extension],
    )
    scanned_sanitary_card = models.FileField(
        upload_to=upload_to_scanned_sanitary_card,
        null=True,
        blank=True,
        validators=[validate_file_extension],
    )
    nationality = models.CharField(max_length=255)
    birthdate = models.DateField()
    is_morning_student = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING, null=True)
    activities_during_exit = models.CharField(max_length=1000, null=True, blank=True)
    avatar = models.FileField(
        upload_to=upload_to_avatar,
        validators=[validate_image_extension],
        null=True,
        blank=True,
    )
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
    marks = models.FileField(
        upload_to=upload_to_quartermarks,
        null=True,
        blank=True,
        validators=[validate_file_extension],
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="quarter_marks"
    )


class Partner(models.Model):
    address = models.CharField(max_length=255, null=True, blank=True)
    enrollment_document = models.FileField(
        upload_to=upload_to_partner,
        null=True,
        blank=True,
        validators=[validate_file_extension],
    )
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
        upload_to=upload_to_quota_extension_document,
        validators=[validate_file_extension],
        null=True,
        blank=True,
    )
    date = models.DateField()
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name="donations"
    )


class PunctualDonation(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField()
    proof_of_payment_document = models.FileField(
        upload_to=upload_to_punctual_donation,
        validators=[validate_file_extension],
    )
    date = models.DateField(auto_now_add=True, blank=True)


class HomeDocument(models.Model):
    title = models.CharField(max_length=255)
    document = models.FileField(
        upload_to="home_document",
        null=True,
        blank=True,
    )
    date = models.DateField()


class Volunteer(models.Model):
    academic_formation = models.CharField(max_length=1000)
    motivation = models.CharField(max_length=1000)
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    enrollment_document = models.FileField(
        upload_to=upload_to_enrollment_document,
        validators=[validate_file_extension],
    )
    registry_sheet = models.FileField(
        upload_to=upload_to_registry_sheet,
        validators=[validate_file_extension],
    )
    sexual_offenses_document = models.FileField(
        upload_to=upload_to_sexual_offenses,
        validators=[validate_file_extension],
    )
    scanned_id = models.FileField(
        upload_to=upload_to_scanned_id,
        validators=[validate_file_extension],
    )
    minor_authorization = models.FileField(
        upload_to=upload_to_minor_authorization,
        validators=[validate_file_extension],
    )
    scanned_authorizer_id = models.FileField(
        upload_to=upload_to_scanned_authorizer_id,
        validators=[validate_file_extension],
    )
    birthdate = models.DateField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


class Educator(models.Model):
    birthdate = models.DateField(null=True)


class CustomUserManager(UserManager):
    def create_user(self, email, username="None", password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        if "id_number" not in extra_fields:
            extra_fields.setdefault("is_enabled", False)

        user = super().create_user(
            username=username, email=email, password=password, **extra_fields
        )
        user.username = None

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username="None", password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        user = super().create_superuser(
            username=username, email=email, password=password, **extra_fields
        )
        user.username = None
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = CustomUserManager()

    username = models.CharField(max_length=100, null=True, blank=True)
    id_number = models.CharField(max_length=9, null=True)
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
    avatar = models.FileField(
        upload_to=upload_to_avatar,
        validators=[validate_image_extension],
    )
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

    is_enabled = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


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
    students = models.ManyToManyField(Student, related_name="lessons", blank=True)
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
    price = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    educators = models.ManyToManyField(Educator, related_name="lesson_events")
    attendees = models.ManyToManyField(
        Student, related_name="lesson_events", blank=True
    )
    volunteers = models.ManyToManyField(
        Volunteer, related_name="lesson_events", blank=True
    )


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    place = models.CharField(max_length=1000)
    max_volunteers = models.IntegerField(validators=[MinValueValidator(0)])
    max_attendees = models.IntegerField(validators=[MinValueValidator(0)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    attendees = models.ManyToManyField(Student, related_name="events", blank=True)
    volunteers = models.ManyToManyField(Volunteer, related_name="events", blank=True)


class CenterExitAuthorization(models.Model):
    authorization = models.FileField(
        upload_to=upload_to_authorization,
        validators=[validate_file_extension],
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="center_exits"
    )
    is_authorized = models.BooleanField(default=False)
    lesson_event = models.ForeignKey(
        LessonEvent, on_delete=models.CASCADE, related_name="center_exit_authorizations"
    )


class Suggestion(models.Model):
    subject = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
