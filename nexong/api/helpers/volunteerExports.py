from ..Donation.views import CreateTableFromResponse
import csv
from openpyxl import Workbook
from reportlab.lib.pagesizes import A3, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
)
import zipfile
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
import io
from ...models import User

def obtainDataFromRequest(request, returnOnlyUserList=False):
    # Filter ignores caps in name and surname but status being a enum should be exact
    name = request.GET.get("name", None)
    surname = request.GET.get("surname", None)
    status = request.GET.get("status", None)
    args = {}
    args["role__in"] = ["VOLUNTARIO", "VOLUNTARIO_SOCIO"]
    if name is not None:
        args["first_name__iexact"] = name
    if surname is not None:
        args["last_name__iexact"] = surname
    if status is not None:
        args["volunteer__status"] = status
    queryset = User.objects.filter(**args)
    if returnOnlyUserList:
        return queryset
    filename = "Datos de los voluntarios"
    objects = []
    for user in queryset:
        objects.append(
            [
                user.first_name,
                user.last_name,
                user.volunteer.status,
                user.volunteer.start_date,
                user.volunteer.end_date,
                user.volunteer.academic_formation,
                user.volunteer.motivation,
                user.volunteer.address,
                user.volunteer.postal_code,
                user.volunteer.birthdate,
            ]
        )

    return (
        objects,
        filename,
    )


def VolunteersExportToCsv(request):
    response = HttpResponse(content_type="text/csv")
    data, filename = obtainDataFromRequest(request)
    response["Content-Disposition"] = f"attachment; filename={filename}.csv"

    writer = csv.writer(response)

    writer.writerow(
        [
            "Nombre",
            "Apellidos",
            "Estado",
            "Fecha de comienzo",
            "Fecha de salida",
            "Formación académica",
            "Motivación",
            "Domicilio",
            "Código postal",
            "Fecha de Nacimiento",
        ]
    )
    for row in data:
        writer.writerow(row)

    return response


def CreateResponseObject(filename):
    # Response Object
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename={filename}.pdf"
    styles = getSampleStyleSheet()

    # This is the PDF document
    doc = SimpleDocTemplate(
        response, pagesize=landscape(A3), title="Datos de los voluntarios"
    )

    # Create a Story list to hold elements
    Story = []

    # Add cover page elements
    logoPath = "static/images/logo.png"
    logo = Image(logoPath, width=200, height=100)
    return (
        response,
        styles,
        doc,
        Story,
        logo,
    )


def CreateCoverElements(logo, title, styles, Story):
    cover_elements = [
        logo,
        Spacer(1, 12),
        Paragraph(title, styles["Title"]),
    ]

    # Add cover elements to the Story
    Story.extend(cover_elements)
    # Separation for the table
    Story.append(Spacer(1, 50))
    return Story


def VolunteersExportToPdf(request):
    data = obtainDataFromRequest(request)

    # Unpack values
    data, filename = obtainDataFromRequest(request)

    dataFromResponse = CreateResponseObject(filename)
    (
        response,
        styles,
        doc,
        Story,
        logo,
    ) = dataFromResponse[:5]
    title = f"Datos de los voluntarios"

    StoryUpdated = CreateCoverElements(
        logo,
        title,
        styles,
        Story,
    )
    table_data = [
        [
            "Nombre",
            "Apellidos",
            "Estado",
            "Fecha de comienzo",
            "Fecha de salida",
            "Formación académica",
            "Motivación",
            "Domicilio",
            "Código postal",
            "Fecha de Nacimiento",
        ]
    ]

    for row in data:
        table_data.append(row)

    CreateTableFromResponse(table_data, StoryUpdated, doc)

    return response


def VolunteersExportToExcel(request):
    data = obtainDataFromRequest(request)

    data, filename = obtainDataFromRequest(request)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename={filename}.xlsx"

    # Create a new Excel workbook
    workbook = Workbook()
    sheet = workbook.active

    header_row = [
        "Nombre",
        "Apellidos",
        "Estado",
        "Fecha de comienzo",
        "Fecha de salida",
        "Formación académica",
        "Motivación",
        "Domicilio",
        "Código postal",
        "Fecha de Nacimiento",
    ]
    sheet.append(header_row)

    for row in data:
        sheet.append(row)

    # Save the workbook to the response
    workbook.save(response)

    return response


def Download_files(request):
    # Get files
    queryset = obtainDataFromRequest(request, True)
    buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(buffer, "w")
    # Iterate over queryset
    for user in queryset:
        user_folder = user.last_name + " " + user.first_name  # file for each volunteer
        if user.volunteer.enrollment_document:
            zip_file.writestr(
                user_folder + "/" + "Documento de inscripción.pdf",
                user.volunteer.enrollment_document.read(),
            )
        if user.volunteer.registry_sheet:
            zip_file.writestr(
                user_folder + "/" + "Hoja de registro.pdf",
                user.volunteer.registry_sheet.read(),
            )
        if user.volunteer.sexual_offenses_document:
            zip_file.writestr(
                user_folder + "/" + "Documentos de delitos sexuales.pdf",
                user.volunteer.sexual_offenses_document.read(),
            )
        if user.volunteer.scanned_id:
            zip_file.writestr(
                user_folder + "/" + "DNI escaneado.pdf",
                user.volunteer.scanned_id.read(),
            )
        if user.volunteer.minor_authorization:
            zip_file.writestr(
                user_folder + "/" + "Autorización de menores.pdf",
                user.volunteer.minor_authorization.read(),
            )
        if user.volunteer.scanned_authorizer_id:
            zip_file.writestr(
                user_folder + "/" + "Identificación autorizada escaneada.pdf",
                user.volunteer.scanned_authorizer_id.read(),
            )

    zip_file.close()

    # Return zip
    response = HttpResponse(buffer.getvalue())
    response["Content-Type"] = "application/x-zip-compressed"
    response["Content-Disposition"] = "attachment; filename=Fichas Voluntarios.zip"

    return response