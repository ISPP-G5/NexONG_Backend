import io
from django.utils.http import urlsafe_base64_decode
import requests
from django.views import View
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from ..Donation.views import CreateTableFromResponse
from .authSerializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
import csv
from openpyxl import Workbook
from reportlab.lib.pagesizes import A3, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
import zipfile
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from ..permissions import *


def process_instance(serializer_class, instance, data):
    serializer = serializer_class(instance, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserApiViewSet(ModelViewSet):
    http_method_names = ["get", "put", "delete"]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [isAdmin]


class EducatorApiViewSet(ModelViewSet):
    queryset = Educator.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = EducatorSerializer
    permission_classes = [isAdmin | isEducator]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PartnerApiViewSet(ModelViewSet):
    queryset = Partner.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = PartnerSerializer
    permission_classes = [isAdmin | isPartner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class VolunteerApiViewSet(ModelViewSet):
    queryset = Volunteer.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = VolunteerSerializer
    permission_classes = [isAdmin | isVolunteer]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


def obtainDataFromRequest(request):
    queryset = User.objects.filter(role__in=["VOLUNTARIO", "VOLUNTARIO_SOCIO"])
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
    zipo = {}
    zipo["Datos de los voluntarios.pdf"] = VolunteersExportToPdf(request)
    zipo["Datos de los voluntarios.csv"] = VolunteersExportToCsv(request)
    zipo["Datos de los voluntarios.xlsx"] = VolunteersExportToExcel(request)
    # Create zip
    buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(buffer, "w")
    for k, v in zipo.items():
        zip_file.writestr(k, v.content)
    zip_file.close()
    # Return zip
    response = HttpResponse(buffer.getvalue())
    response["Content-Type"] = "application/x-zip-compressed"
    response["Content-Disposition"] = "attachment; filename=voluntarios.zip"

    return response


class FamilyApiViewSet(ModelViewSet):
    queryset = Family.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = FamilySerializer
    permission_classes = [isAdmin | isFamily]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EducationCenterApiViewSet(ModelViewSet):
    queryset = EducationCenter.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = EducationCenterSerializer
    permission_classes = [isAdmin | isEducationCenter]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RedirectSocial(View):
    def get(self, request, *args, **kwargs):
        code, state = str(request.GET["code"]), str(request.GET["state"])
        json_obj = {"code": code, "state": state}
        return JsonResponse(json_obj)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    authentication_classes = ()
    serializer_class = LogoutAndBlacklistSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data["refresh_token"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserView(APIView):
    authentication_classes = ()
    serializer_class = ActivateSerializer

    def post(self, request):
        access_token = request.headers.get("Authorization")
        url = "http://localhost:8000/api/auth/users/me"  # Actualiza con la URL de tu aplicación
        headers = {"Authorization": access_token}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    id_number = serializer.validated_data["id_number"]
                    email = response.json()["email"]
                    user = User.objects.get(email=email)
                    if not user.is_enabled and not user.id_number:
                        user.id_number = id_number
                        user.is_enabled = True
                        user.save()
                        return Response(status=status.HTTP_200_OK)
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=response.status_code)


class CustomActivateView(APIView):
    def post(self, request, *args, **kwargs):
        uid = kwargs.get("uid")
        token = kwargs.get("token")
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
            if not user.is_enabled:
                if default_token_generator.check_token(user, token):
                    user.is_enabled = True
                    user.is_active = True
                    user.save()
                return Response(status=status.HTTP_200_OK)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Token not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
