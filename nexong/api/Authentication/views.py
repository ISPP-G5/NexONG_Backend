import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from src import settings
from ...models import *
from rest_framework.permissions import AllowAny
from .authSerializer import *
from auth0.authentication import Database, GetToken
from auth0.exceptions import Auth0Error, RateLimitError
from auth0.management import Auth0

"""
def process_instance(serializer_class, instance, data):
    serializer = serializer_class(instance, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserApiViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = UserSerializer
    queryset = User.objects.all()
"""


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.pop("email")
        password = serializer.validated_data.pop("password")

        custom_fields = {
            field: serializer.validated_data.pop(field)
            for field in ("name", "surname", "id_number", "role", "phone", "avatar")
        }

        try:
            # Create user instance with custom fields
            user = User.objects.create_user(
                email=email, password=password, **custom_fields
            )

            # register user in auth0
            db = Database(settings.AUTH0_DOMAIN, settings.AUTH0_CLIENT_ID)
            resp = db.signup(
                email=user.email,
                password=password,
                name=user.name,
                surname=user.surname,
                id_number=user.id_number,
                role=user.role,
                phone=user.phone,
                avatar=user.avatar,
                connection="Username-Password-Authentication",
            )
            logging.info(f"Auth0 API signup response => {resp}")
            user.auth0_id = "auth0|" + resp["_id"]

            # get roles from auth0
            mgmt_auth = Auth0(settings.AUTH0_DOMAIN, settings.AUTH0_MMT_API_TOKEN)
            role_id = mgmt_auth.roles.list()["roles"][0]["id"]
            user.role_id = role_id
            user.save()

            # assign role to user in auth0
            mgmt_auth.roles.add_users(role_id, users=[user.auth0_id])
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        except (Auth0Error, RateLimitError) as e:
            logging.info(f"Auth0 signup error resp => {str(e)}")
            user.delete()
            return Response(
                {
                    "message": "Something went wrong while creating the user. Please try again.",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class EducatorApiViewSet(ModelViewSet):
    queryset = Educator.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = EducatorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PartnerApiViewSet(ModelViewSet):
    queryset = Partner.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = PartnerSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class VolunteerApiViewSet(ModelViewSet):
    queryset = Volunteer.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = VolunteerSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FamilyApiViewSet(ModelViewSet):
    queryset = Family.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = FamilySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EducationCenterApiViewSet(ModelViewSet):
    queryset = EducationCenter.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = EducationCenterSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
