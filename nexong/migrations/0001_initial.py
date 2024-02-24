# Generated by Django 5.0.2 on 2024-02-24 17:48

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Educator",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("birthdate", models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Family",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Partner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("holder", models.CharField(max_length=255)),
                ("iban", models.CharField(max_length=34, unique=True)),
                (
                    "quantity",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("ANNUAL", "Anual"),
                            ("MENSUAL", "Mensual"),
                            ("QUARTERLY", "Trimestral"),
                            ("SIX-MONTHLY", " Seis Meses"),
                        ],
                        default="MENSUAL",
                        max_length=11,
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("enrollment_document", models.FileField(upload_to="")),
                (
                    "quota_extension_document",
                    models.FileField(blank=True, null=True, upload_to=""),
                ),
                ("birthdate", models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Volunteer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("academic_formation", models.CharField(max_length=1000)),
                ("motivation", models.CharField(max_length=1000)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pendiente"),
                            ("ACCEPTED", "Aceptado"),
                            ("REJECTED", "Rechazado"),
                        ],
                        default="PENDING",
                        max_length=10,
                    ),
                ),
                ("address", models.CharField(max_length=255)),
                (
                    "postal_code",
                    models.IntegerField(
                        default=10000,
                        validators=[
                            django.core.validators.MinValueValidator(10000),
                            django.core.validators.MaxValueValidator(90000),
                        ],
                    ),
                ),
                ("enrollment_document", models.FileField(upload_to="")),
                ("registry_sheet", models.FileField(upload_to="")),
                ("sexual_offenses_document", models.FileField(upload_to="")),
                ("scanned_id", models.FileField(upload_to="")),
                (
                    "minor_authorization",
                    models.FileField(blank=True, null=True, upload_to=""),
                ),
                (
                    "scanned_authorizer_id",
                    models.FileField(blank=True, null=True, upload_to=""),
                ),
                ("birthdate", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=1000)),
                (
                    "capacity",
                    models.IntegerField(
                        blank=True,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("is_morning_lesson", models.BooleanField(default=True)),
                (
                    "educator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="nexong.educator",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=1000)),
                ("place", models.CharField(max_length=1000)),
                (
                    "capacity",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "max_volunteers",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("start_date", models.DateTimeField(blank=True)),
                ("end_date", models.DateTimeField(blank=True)),
                (
                    "lesson",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nexong.lesson",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LessonEvaluation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=1000)),
                (
                    "grade_system",
                    models.CharField(
                        choices=[
                            ("ZERO_TO_ONE", "0-1"),
                            ("ONE_TO_FIVE", "1-5"),
                            ("ZERO_TO_TEN", "0-10"),
                        ],
                        default="ZERO_TO_TEN",
                        max_length=20,
                    ),
                ),
                (
                    "grade",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                ("date", models.DateField()),
                (
                    "evaluation_type",
                    models.CharField(
                        choices=[("DAILY", "Diario"), ("ANNUAL", "Anual")],
                        default="DAILY",
                        max_length=10,
                    ),
                ),
                (
                    "family",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lesson_evaluations",
                        to="nexong.family",
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lesson_evaluations",
                        to="nexong.lesson",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Meeting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=1000)),
                ("date", models.DateField(blank=True)),
                ("time", models.DateTimeField(blank=True)),
                (
                    "attendees",
                    models.ManyToManyField(
                        related_name="meetings_attending", to="nexong.partner"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("education_center", models.CharField(max_length=255)),
                (
                    "current_education_year",
                    models.CharField(
                        choices=[
                            ("THREE_YEARS", "Tres años"),
                            ("FOUR_YEARS", "Cuatro años"),
                            ("FIVE_YEARS", "Cinco años"),
                            ("FIRST_PRIMARY", "Primero de primaria"),
                            ("SECOND_PRIMARY", "Segundo de primaria"),
                            ("THIRD_PRIMARY", "Tercero de primaria"),
                            ("FOURTH_PRIMARY", "Cuarto de primaria"),
                            ("FIFTH_PRIMARY", "Quinto de primaria"),
                            ("SIXTH_PRIMARY", "Sexto de primaria"),
                            ("FIRST_SECONDARY", "Primero de secundaria"),
                            ("SECOND_SECONDARY", "Segundo de secundaria"),
                            ("THIRD_SECONDARY", "Tercero de secundaria"),
                            ("FOURTH_SECONDARY", "Cuarto de secundaria"),
                        ],
                        default="THREE_YEARS",
                        max_length=20,
                    ),
                ),
                ("education_center_tutor", models.CharField(max_length=255)),
                ("enrollment_document", models.FileField(upload_to="")),
                ("scanned_sanitary_card", models.FileField(upload_to="")),
                ("nationality", models.CharField(max_length=255)),
                ("birthdate", models.DateField()),
                (
                    "family",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="students",
                        to="nexong.family",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="lesson",
            name="students",
            field=models.ManyToManyField(related_name="lessons", to="nexong.student"),
        ),
        migrations.CreateModel(
            name="CenterExitAuthorization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("authorization", models.FileField(upload_to="")),
                ("is_authorized", models.BooleanField(default=False)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="center_exit_authorizations",
                        to="nexong.event",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="center_exits",
                        to="nexong.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StudentEvaluation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=1000)),
                (
                    "grade_system",
                    models.CharField(
                        choices=[
                            ("ZERO_TO_ONE", "0-1"),
                            ("ONE_TO_FIVE", "1-5"),
                            ("ZERO_TO_TEN", "0-10"),
                        ],
                        default="ZERO_TO_TEN",
                        max_length=20,
                    ),
                ),
                (
                    "grade",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                ("date", models.DateField()),
                (
                    "evaluation_type",
                    models.CharField(
                        choices=[("DAILY", "Diario"), ("ANNUAL", "Anual")],
                        default="DAILY",
                        max_length=10,
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student_evaluations",
                        to="nexong.lesson",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student_evaluations",
                        to="nexong.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("surname", models.CharField(max_length=100)),
                ("id_number", models.CharField(max_length=9, unique=True)),
                (
                    "phone",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MaxValueValidator(999999999),
                            django.core.validators.MinValueValidator(600000000),
                        ],
                    ),
                ),
                ("password", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("ADMIN", "Administrador"),
                            ("VOLUNTEER", "Voluntario"),
                            ("EDUCATOR", "Educador"),
                            ("FAMILY", "Familia"),
                            ("PARTNER", "Socio"),
                            ("VOLUNTEER_PARTNER", "Voluntario y socio"),
                        ],
                        default="FAMILY",
                        max_length=25,
                    ),
                ),
                (
                    "avatar",
                    models.URLField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.URLValidator()],
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "educator",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nexong.educator",
                    ),
                ),
                (
                    "family",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nexong.family",
                    ),
                ),
                (
                    "partner",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nexong.partner",
                    ),
                ),
                (
                    "volunteer",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nexong.volunteer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="event",
            name="attendees",
            field=models.ManyToManyField(related_name="events", to="nexong.user"),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "commentee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments_received",
                        to="nexong.user",
                    ),
                ),
                (
                    "commenter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments_made",
                        to="nexong.user",
                    ),
                ),
            ],
        ),
    ]
