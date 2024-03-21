from rest_framework.viewsets import ModelViewSet
from nexong.api.Student.studentSerializer import (
    StudentSerializer,
    QuarterMarksSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from nexong.models import Student, QuarterMarks
import csv
import codecs
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


class StudentApiViewSet(ModelViewSet):
    queryset = Student.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuarterMarksApiViewSet(ModelViewSet):
    queryset = QuarterMarks.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = QuarterMarksSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


def StudentsExportToCsv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="Datos_Estudiantes.csv"'

    # Open the CSV file with UTF-8 encoding
    response.write(codecs.BOM_UTF8)

    # Create a CSV writer object
    writer = csv.writer(response, csv.excel)

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
        writer.writerow(
            [
                smart_str(student.name),
                smart_str(student.surname),
                smart_str(student.current_education_year),
                smart_str(student.nationality),
                smart_str(student.birthdate),
                smart_str(student.is_morning_student),
                smart_str(student.status),
                smart_str(student.education_center),
                smart_str(student.family),
            ]
        )

    return response


def obtainDataFromRequest(request):
    # Get data from request
    name = request.GET.get("name")
    surname = request.GET.get("surname")
    family = request.GET.get("family")
    nationality = request.GET.get("nationality")
    morning = request.GET.get("morning")

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
    # Filter donations
    if (
        name is None
        and surname is None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.all()
        filename = "Reporte de estudiantes global."
    elif (
        name is None
        and surname is None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(is_morning_student=morning)
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
        and surname is None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(family__name__icontains=family)
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
        and surname is None
        and nationality is None
        and family is not None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            family__name__icontains=family, is_morning_student=morning
        )
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
        and surname is None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(nationality__icontains=nationality)
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
        and surname is None
        and nationality is not None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            nationality__icontains=nationality, is_morning_student=morning
        )
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
        and surname is None
        and nationality is not None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            nationality__icontains=nationality, family__name__icontains=family
        )
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
        and surname is not None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(surname__icontains=surname)
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
        and surname is not None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            surname__icontains=surname, is_morning_student=morning
        )
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
        and surname is not None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            surname__icontains=surname, family__name__icontains=family
        )
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
        and surname is not None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            surname__icontains=surname, nationality__icontains=nationality
        )
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is None
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
        filename = "Reporte_de_estudiantes."

    elif (
        name is not None
        and surname is None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(name__icontains=name)
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
        and surname is None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            name__icontains=name, is_morning_student=morning
        )
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
        and surname is None
        and nationality is None
        and family is not None
        and morning is None
    ):
        queryset = Student.objects.filter(
            name__icontains=name, family__name__icontains=family
        )
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
        and surname is None
        and nationality is not None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            name__icontains=name, nationality__icontains=nationality
        )
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
        and surname is not None
        and nationality is None
        and family is None
        and morning is None
    ):
        queryset = Student.objects.filter(
            name__icontains=name, surname__icontains=surname
        )
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
        and surname is not None
        and nationality is None
        and family is None
        and morning is not None
    ):
        queryset = Student.objects.filter(
            name__icontains=name, surname__icontains=surname, is_morning_student=morning
        )
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
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
        filename = "Reporte_de_estudiantes."
    elif (
        name is not None
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
        filename = "Reporte_de_estudiantes."
    else:
        queryset = Student.objects.filter(
            name__icontains=name,
            surname__icontains=surname,
            nationality__icontains=nationality,
            family__name__icontains=family,
            is_morning_student=morning,
        )
        filename = "Reporte de estudiantes."

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
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename={filename}.pdf"
    styles = getSampleStyleSheet()

    # This is the PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Create a Story list to hold elements
    Story = []

    # Add cover page elements
    logoPath = "static/images/logo.png"
    logo = Image(logoPath, width=200, height=100)
    title = "Estudiantes"
    actualDateText = f"Fecha actual: {actualDate}"

    cover_elements = [
        logo,
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
        # Truncate long strings
        table_row = [
            student.name[:15]
            if isinstance(student.name, str) and len(student.name) > 15
            else student.name,
            student.surname[:15]
            if isinstance(student.surname, str) and len(student.surname) > 15
            else student.surname,
            student.current_education_year[:15]
            if isinstance(student.current_education_year, str)
            and len(student.current_education_year) > 15
            else student.current_education_year,
            student.nationality[:15]
            if isinstance(student.nationality, str) and len(student.nationality) > 15
            else student.nationality,
            str(student.birthdate)[:15]
            if isinstance(student.birthdate, str) and len(str(student.birthdate)) > 15
            else student.birthdate,
            student.is_morning_student,
            student.status,
            student.education_center.name[:20]
            if isinstance(student.education_center, str)
            and len(student.education_center) > 20
            else student.education_center.name,
            student.family[:20]
            if isinstance(student.family, str) and len(student.family) > 20
            else student.family,
        ]
        table_data.append(table_row)

    # Create a table
    table = Table(
        table_data, colWidths=[40, 60, 90, 50, 45, 45, 60, 133, 80]
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

    return response


def StudentsExportToExcel(request):
    data = obtainDataFromRequest(request)

    # Unpack values
    (
        queryset,
        filename,
    ) = data[:2]

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename={filename}.xlsx"

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
    workbook.save(response)

    return response
