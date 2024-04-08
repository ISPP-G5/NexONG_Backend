import csv
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from ...models import User


def CreateTableFromResponse(table_data, Story, doc):
    # Create a table
    table = Table(table_data)

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
             ]
        )
     )

    # Table to Story
    Story.append(table)
    doc.build(Story)


def obtainDataFromRequest(request, returnOnlyUserList=False):
    # Filter ignores caps in name and surname but status being a enum should be exact
    name = request.GET.get("name", None)
    surname = request.GET.get("surname", None)
    args = {}
    args["role__in"] = ["SOCIO"]
    if name is not None:
        args["first_name__iexact"] = name
    if surname is not None:
        args["last_name__iexact"] = surname
    queryset = User.objects.filter(**args)
    if returnOnlyUserList:
        return queryset
    filename = "Datos de los socios"
    objects = []
    for user in queryset:
        objects.append(
            [
                user.first_name,
                user.last_name,
                user.email,
                user.phone,
                user.partner.address,
                user.partner.birthdate,
            ]
        )

    return (
        objects,
        filename,
    )


def PartnersExportToCsv(request):
    response = HttpResponse(content_type="text/csv")
    data, filename = obtainDataFromRequest(request)
    response["Content-Disposition"] = f"attachment; filename={filename}.csv"

    writer = csv.writer(response)

    writer.writerow(
        [
            "Nombre",
            "Apellidos",
            "Correo",
            "Teléfono",
            "Domicilio",
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
        response, pagesize=portrait(A4), title="Datos de los socios"
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


def PartnersExportToPdf(request):
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
    title = f"Datos de los socios"

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
            "Correo",
            "Teléfono",
            "Domicilio",
            "Fecha de Nacimiento",
        ]
    ]

    for row in data:
        table_data.append(row)

    CreateTableFromResponse(table_data, StoryUpdated, doc)

    return response


def PartnersExportToExcel(request):
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
        "Correo",
        "Teléfono",
        "Domicilio",
        "Fecha de Nacimiento",
    ]
    sheet.append(header_row)

    for row in data:
        sheet.append(row)

    # Save the workbook to the response
    workbook.save(response)

    return response
