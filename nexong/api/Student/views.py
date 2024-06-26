from rest_framework.viewsets import ModelViewSet
from nexong.api.Student.studentSerializer import (
    StudentSerializer,
    QuarterMarksSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from ..permissions import *
import csv
import codecs
from datetime import timedelta, date
from django.http import HttpResponse
from django.utils.encoding import smart_str
from datetime import datetime
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def update_student_status(student):
    if student.acceptance_date and (
        student.acceptance_date + timedelta(days=365) <= date.today()
    ):
        student.status = "CADUCADO"
        student.save()


class StudentApiViewSet(ModelViewSet):
    queryset = Student.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = StudentSerializer
    permission_classes = [isFamily | isEducatorGet | isEducationCenter | isAdmin]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        update_student_status(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuarterMarksApiViewSet(ModelViewSet):
    queryset = QuarterMarks.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = QuarterMarksSerializer
    permission_classes = [
        isFamily | isEducatorGet | isEducationCenter | isAdminGetPutAndDelete
    ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


def StudentsExportToCsv(request):
    response_csv = HttpResponse(content_type="text/csv")
    response_csv["Content-Disposition"] = 'attachment; filename="Datos_Estudiantes.csv"'

    # Open the CSV file with UTF-8 encoding
    response_csv.write(codecs.BOM_UTF8)

    # Create a CSV writer object
    writer = csv.writer(response_csv, csv.excel)

    # Write the header row
    writer.writerow(
        [
            smart_str("Nombre"),
            smart_str("Apellido"),
            smart_str("Curso Actual"),
            smart_str("Nacionalidad"),
            smart_str("Fecha de Nacimiento"),
            smart_str("Estudiante de Mañana"),
            smart_str("Estado"),
            smart_str("Centro Educativo"),
            smart_str("Familia"),
        ]
    )

    # Retrieve data from your model
    queryset = Student.objects.all()

    # Write data rows
    for student in queryset:
        update_student_status(student)
        writer.writerow(
            [
                smart_str(student.name),
                smart_str(student.surname),
                smart_str(student.current_education_year),
                smart_str(student.nationality),
                smart_str(student.birthdate),
                smart_str(student.is_morning_student),
                smart_str(student.status),
                smart_str(student.education_center.name),
                smart_str(student.family.name),
            ]
        )

    return response_csv


def obtainDataFromRequest(request):
    # Get data from request
    name = request.GET.get("name")
    surname = request.GET.get("surname")
    family = request.GET.get("family")
    nationality = request.GET.get("nationality")
    morning = request.GET.get("morning")
    status = request.GET.get("status")
    education_year = request.GET.get("education_year")

    # Comprobe if data exist
    if not name:
        name = None
    else:
        name = name
    if not surname:
        surname = None
    else:
        surname = surname
    if not nationality:
        nationality = None
    else:
        nationality = nationality
    if not family:
        family = None
    else:
        family = family
    if not morning:
        morning = None
    else:
        morning = morning
    if not status:
        status = None
    else:
        if status not in dict(STATUS).keys():
            status = None
        else:
            status = status
    if not education_year:
        education_year = None
    else:
        if education_year not in dict(CURRENT_EDUCATION_YEAR).keys():
            education_year = None
        else:
            education_year = education_year

    if (
        status is None
        and education_year is None
        and name is None
        and surname is None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.all()
        filename = "Reporte de estudiantes global."
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(is_morning_student=morning)
        filename = f"Reporte de estudiantes de por la mañana {morning}"
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(family__name__icontains=family)
        filename = f"Reporte de estudiantes de familia {family}"
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            family__name__icontains=family, is_morning_student=morning
        )
        filename = f"Reporte de studiantes por la mañana {morning} y familia {family}"
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(nationality__icontains=nationality)
        filename = f"Reporte de estudiantes de nacionalidad {nationality}"
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            nationality__icontains=nationality, is_morning_student=morning
        )
        filename = f"Reporte de estudiantes de nacionalidad {nationality} y por la mañana {morning}"
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            nationality__icontains=nationality, family__name__icontains=family
        )
        filename = (
            f"Reporte de estudiantes de nacionalidad {nationality} y familia {family}"
        )
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte de estudiantes de nacionalidad {nationality}, por la mañana {morning} y familia {family}"
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(surname__icontains=surname)
        filename = f"Reporte_de_estudiantes apellido {surname}"
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            surname__icontains=surname, is_morning_student=morning
        )
        filename = (
            f"Reporte_de_estudiantes apellido {surname} y por la mañana {morning}"
        )
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            surname__icontains=surname, family__name__icontains=family
        )
        filename = f"Reporte_de_estudiantes apellido {surname} y familia {family}"
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            surname__icontains=surname,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes apellido {surname}, por la mañana {morning} y familia {family}"
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            surname__icontains=surname, nationality__icontains=nationality
        )
        filename = (
            f"Reporte_de_estudiantes apellido {surname} y nacionalidad {nationality}"
        )
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            surname__icontains=surname,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes apellido {surname}, por la mañana {morning} y nacionalidad {nationality}"
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes apellido {surname}, familia {family} y nacionalidad {nationality}"
    elif (
        status is None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes apellido {surname}, por la mañana {morning}, nacionalidad {nationality} y familia{family}"

    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(name__icontains=name)
        filename = f"Reporte_de_estudiantes nombre {name}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            name__icontains=name, is_morning_student=morning
        )
        filename = f"Reporte_de_estudiantes nombre {name} y por la mañana {morning}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            name__icontains=name, family__name__icontains=family
        )
        filename = f"Reporte_de_estudiantes nombre {name} y familia {family}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            name__icontains=name,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes nombre {name}, por la mañana {morning} y familia {family}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            name__icontains=name, nationality__icontains=nationality
        )
        filename = f"Reporte_de_estudiantes nombre {name} y nacionalidad {nationality}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            name__icontains=name,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes nombre {name}, por la mañana {morning} y nacionalidad {nationality}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            name__icontains=name,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes nombre {name}, nacionalidad {nationality} y familia {family}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            name__icontains=name,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes nombre {name}, nacionalidad {nationality}, familia {family} y por la mañana {morning}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            name__icontains=name, surname__icontains=surname
        )
        filename = f"Reporte_de_estudiantes nombre {name} y apellido {surname}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            name__icontains=name, surname__icontains=surname, is_morning_student=morning
        )
        filename = f"Reporte_de_estudiantes nombre {name}, apellido {surname} y por la mañana {morning}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            name__icontains=name,
            surname__icontains=surname,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes nombre {name}, apellido {surname} y familia {family}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            name__icontains=name,
            surname__icontains=surname,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes nombre {name}, apellido {surname}, familia {family} y por la mañana {morning}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
        )
        filename = f"Reporte_de_estudiantes nombre {name}, apellido {surname} y nacionalidad {nationality}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes nombre {name}, apellido {surname}, nacionalidad {nationality} y por la mañana {morning}"
    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes nombre {name}, apellido {surname}, nacionalidad {nationality} y familia {family}"

    elif (
        status is None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes nombre {name}, apellido{surname}, nacionalidad {nationality}, familia {family}, por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(current_education_year=education_year)
        filename = f"Reporte_de_estudiantes año {education_year}"
    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year, is_morning_student=morning
        )
        filename = (
            f"Reporte_de_estudiantes año {education_year} y por la mañana {morning}"
        )
    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year, family__name__icontains=family
        )
        filename = f"Reporte_de_estudiantes año {education_year} y familia {family}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año{education_year}, familia {family} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year, nationality__icontains=nationality
        )
        filename = (
            f"Reporte_de_estudiantes año {education_year} y nacionalidad {nationality}"
        )

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año{education_year}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nacionalidad {nationality} y familia {family}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year},nacionalidad {nationality}, familia {family} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            surname__icontains=surname,
        )
        filename = f"Reporte_de_estudiantes año {education_year}y apellido{surname}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            surname__icontains=surname,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, apellido {surname} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            surname__icontains=surname,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, apellido {surname} y familia {family}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            surname__icontains=surname,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, apellido {surname}, familia {family} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            surname__icontains=surname,
            nationality__icontains=nationality,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, apellido {surname} y nacionalidad {nationality}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            surname__icontains=surname,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, apellido {surname}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            surname__icontains=surname,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, apellido {surname}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, apellido {surname}, nacionalidad {nationality} y familia {family}"

    elif (
        status is None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, apellido {surname}, nacionalidad {nationality}, familia {family} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year, name__icontains=name
        )
        filename = f"Reporte_de_estudiantes año {education_year} y nombre {name}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name} y familia {family}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name}, familia {family} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            nationality__icontains=nationality,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name} y nacionalidad {nationality}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name}, nacionalidad {nationality} y familia {family}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name}, nacionalidad {nationality}, familia {family} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            surname__icontains=surname,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name} y surname{surname}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            surname__icontains=surname,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name}, surname{surname} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            surname__icontains=surname,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name}, surname{surname} y familia {family}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            surname__icontains=surname,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name}, surname{surname},familia {family} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name}, surname{surname}, nacionalidad {nationality}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name}, surname{surname}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name}, surname{surname}, nacionalidad {nationality} y familia {family}"

    elif (
        status is None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes año {education_year}, nombre {name}, surname{surname}, nacionalidad {nationality}, familia {family} y por la mañana {morning} "

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status,
        )
        filename = f"Reporte_de_estudiantes estado {status}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(status=status, is_morning_student=morning)
        filename = f"Reporte_de_estudiantes estado {status} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(status=status, family__name__icontains=family)
        filename = f"Reporte_de_estudiantes estado {status} y familia {family}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status, family__name__icontains=family, is_morning_student=morning
        )
        filename = f"Reporte_de_estudiantes estado {status}, familia {family} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status, nationality__icontains=nationality
        )
        filename = (
            f"Reporte_de_estudiantes estado {status} y nacionalidad {nationality}"
        )

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nacionalidad {nationality} y familia {family}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nacionalidad {nationality}, familia {family} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status,
            surname__icontains=surname,
        )
        filename = f"Reporte_de_estudiantes estado {status} y apellido {surname}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status, surname__icontains=surname, is_morning_student=morning
        )
        filename = f"Reporte_de_estudiantes estado {status}, apellido {surname} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status, surname__icontains=surname, family__name__icontains=family
        )
        filename = f"Reporte_de_estudiantes estado {status}, apellido {surname} y familia {family}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            surname__icontains=surname,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, apellido {surname}, familia {family} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status,
            surname__icontains=surname,
            nationality__icontains=nationality,
        )
        filename = f"Reporte_de_estudiantes estado {status}, apellido {surname} y nacionalidad {nationality}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            surname__icontains=surname,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, apellido {surname}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, apellido {surname}, nacionalidad {nationality} y familia {family}"

    elif (
        status is not None
        and education_year is None
        and name is None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, apellido {surname}, nacionalidad {nationality}, familia {family} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(status=status, name__icontains=name)
        filename = f"Reporte_de_estudiantes estado {status} y nombre {name}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status, name__icontains=name, is_morning_student=morning
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status, name__icontains=name, family__name__icontains=family
        )
        filename = (
            f"Reporte_de_estudiantes estado {status}, nombre {name} y familia {family}"
        )

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            name__icontains=name,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name} y familia {family} y por la mañana{morning}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status, name__icontains=name, nationality__icontains=nationality
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name} y nacionalidad {nationality}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            name__icontains=name,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status,
            name__icontains=name,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name}, nacionalidad {nationality} y familia {family}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            name__icontains=name,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name}, nacionalidad {nationality}, familia {family} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status, name__icontains=name, surname__icontains=surname
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name} y apellido {surname}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name}, apellido {surname} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name}, apellido {surname} y familia {family}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name}, apellido {surname}, familia {family} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name}, apellido {surname} y nacionalidad {nationality}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name}, apellido {surname}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name}, apellido {surname}, nacionalidad {nationality} y familia {family}"

    elif (
        status is not None
        and education_year is None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, nombre {name}, apellido {surname}, nacionalidad {nationality}, familia {family} y por la mañana{morning}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
        )
        filename = f"Reporte_de_estudiantes estado {status} y año {education_year}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year} y familia {family}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, familia {family} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            nationality__icontains=nationality,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year} y nacionalidad {nationality}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nacionalidad {nationality} y familia {family}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nacionalidad {nationality}, familia {family} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            surname__icontains=surname,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year} y apellido {surname}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            surname__icontains=surname,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, apellido {surname} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            surname__icontains=surname,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, apellido {surname} y familia {family}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            surname__icontains=surname,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, apellido {surname}, familia {family} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            surname__icontains=surname,
            nationality__icontains=nationality,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, apellido {surname} y nacionalidad {nationality}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            surname__icontains=surname,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, apellido {surname}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, apellido {surname}, nacionalidad {nationality} y familia {family}"

    elif (
        status is not None
        and education_year is not None
        and name is None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, apellido {surname}, nacionalidad {nationality}, familia {family} y por la mañana{morning}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year, status=status, name__icontains=name
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year} y nombre {name}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name} y familia {family}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name}, familia {family} y por la mañana{morning}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            nationality__icontains=nationality,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name} y nacionalidad {nationality}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name}, nacionalidad {nationality} y familia{family}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name}, nacionalidad {nationality}, familia{family} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            surname__icontains=surname,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name} y apellido {surname}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name}, apellido {surname} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name}, apellido {surname} y familia {family}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name}, apellido {surname}, familia {family} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name}, apellido {surname} y nacionalidad {nationality}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name}, apellido {surname}, nacionalidad {nationality} y por la mañana {morning}"

    elif (
        status is not None
        and education_year is not None
        and name is not None
        and surname is not None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name}, apellido {surname}, nacionalidad {nationality} y familia {family}"

    else:
        queryset = Student.objects.filter(
            current_education_year=education_year,
            status=status,
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = f"Reporte_de_estudiantes estado {status}, año {education_year}, nombre {name}, apellido {surname}, nacionalidad {nationality}, familia {family} y por la mañana {morning}"

    return (
        queryset,
        filename,
    )


def StudentsExportToPdf(request):
    actualDate = datetime.now().date()
    data = obtainDataFromRequest(request)

    # Unpack values
    (
        queryset,
        filename,
    ) = data[:2]
    # Response Object
    response_pdf = HttpResponse(content_type="application/pdf")
    response_pdf["Content-Disposition"] = f"attachment; filename={filename}.pdf"
    styles = getSampleStyleSheet()

    # This is the PDF document
    doc = SimpleDocTemplate(response_pdf, pagesize=letter)

    # Create a Story list to hold elements
    Story = []

    # Add cover page elements
    logoPath_pdf = "static/images/logo.png"
    logo_pdf = Image(logoPath_pdf, width=200, height=100)
    title = "Estudiantes"
    actualDateText = f"Fecha actual: {actualDate}"

    cover_elements = [
        logo_pdf,
        Spacer(1, 12),
        Paragraph(title, styles["Title"]),
        Spacer(1, 12),
        Paragraph(actualDateText, styles["Normal"]),
        Spacer(1, 6),
    ]
    # Add cover elements to the Story
    Story.extend(cover_elements)
    # Separation for the table
    Story.append(Spacer(1, 10))
    table_data = [
        [
            "Nombre",
            "Apellido",
            "Curso Actual",
            "Nacionalidad",
            "Nacimiento",
            "De Mañana",
            "Estado",
            "Centro Educativo",
            "Familia",
        ]
    ]

    for student in queryset:
        update_student_status(student)
        # Truncate long strings
        table_row = [
            (
                student.name[:15]
                if isinstance(student.name, str) and len(student.name) > 15
                else student.name
            ),
            (
                student.surname[:15]
                if isinstance(student.surname, str) and len(student.surname) > 15
                else student.surname
            ),
            (
                student.current_education_year[:30]
                if isinstance(student.current_education_year, str)
                and len(student.current_education_year) > 30
                else student.current_education_year
            ),
            (
                student.nationality[:15]
                if isinstance(student.nationality, str)
                and len(student.nationality) > 15
                else student.nationality
            ),
            (
                str(student.birthdate)[:15]
                if isinstance(student.birthdate, str)
                and len(str(student.birthdate)) > 15
                else student.birthdate
            ),
            student.is_morning_student,
            student.status,
            (
                student.education_center.name[:20]
                if isinstance(student.education_center.name, str)
                and len(student.education_center.name) > 20
                else student.education_center.name
            ),
            (
                student.family.name[:20]
                if isinstance(student.family.name, str)
                and len(student.family.name) > 20
                else student.family.name
            ),
        ]
        table_data.append(table_row)

    # Create a table
    table = Table(
        table_data, colWidths=[40, 60, 100, 50, 45, 45, 50, 133, 80]
    )  # Adjust the column width as needed

    # Table style
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 8),  # Adjust the font size as needed
                ("WORDWRAP", (0, 0), (-1, -1), True),  # Allow word wrapping
            ]
        )
    )

    # Table to Story
    Story.append(table)
    doc.build(Story)

    return response_pdf


def StudentsExportToExcel(request):
    data = obtainDataFromRequest(request)

    # Unpack values
    (
        queryset,
        filename,
    ) = data[:2]

    response_excel = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response_excel["Content-Disposition"] = f"attachment; filename={filename}.xlsx"

    # Create a new Excel workbook
    workbook = Workbook()
    sheet = workbook.active

    header_row = [
        "Nombre",
        "Apellido",
        "Curso Actual",
        "Nacionalidad",
        "Nacimiento",
        "De Mañana",
        "Estado",
        "Centro Educativo",
        "Familia",
    ]
    sheet.append(header_row)

    for student in queryset:
        update_student_status(student)
        data_row = [
            student.name,
            student.surname,
            student.current_education_year,
            student.nationality,
            student.birthdate,
            student.is_morning_student,
            student.status,
            student.education_center.name,
            student.family.name,
        ]
        sheet.append(data_row)

    # Save the workbook to the response
    workbook.save(response_excel)

    return response_excel
