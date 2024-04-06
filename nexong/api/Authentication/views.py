import io
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
import requests
from django.views import View
from django.http import Http404, HttpResponse, JsonResponse
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
    Image,
)
import zipfile
from reportlab.lib.styles import getSampleStyleSheet
from ..permissions import *
from django.views.generic import TemplateView


def process_instance(serializer_class, instance, data):
    serializer = serializer_class(instance, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserApiViewSet(ModelViewSet):
    http_method_names = ["get", "put", "delete", "patch"]
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
                user_folder + "/" + "DNI escaneado.pdf", user.volunteer.scanned_id.read()
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
    def get(self, request, *args, **kwargs):
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
                    return redirect(reverse("activation_success"))
                else:
                    return Response(
                        {"detail": "Token not valid"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"detail": "User already activated"}, status=status.HTTP_200_OK
                )
        except User.DoesNotExist:
            raise Http404("User does not exist")
        except requests.exceptions.RequestException as e:
            print("Error making request:", e)
            return Response(
                {"detail": "Error making request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ActivationSuccessView(TemplateView):
    template_name = "custom_activate.html"
