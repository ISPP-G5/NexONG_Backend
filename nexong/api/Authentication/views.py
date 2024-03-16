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
from rest_framework.generics import GenericAPIView


class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        db = Database(settings.AUTH0_DOMAIN, settings.AUTH0_CLIENT_ID)
        email = serializer.validated_data.pop("email")
        password = serializer.validated_data.pop("password")
        user_data = User.objects.create_user(
            email, password, **serializer.validated_data
        )

        try:
            # register user in auth0
            resp = db.signup(
                email=user_data.email,
                password=password,
                name=user_data.name,
                surname=user_data.surname,
                id_number=user_data.id_number,
                role=user_data.role,
                phone=user_data.phone,
                avatar=user_data.avatar,
                connection="Username-Password-Authentication",
            )
            logging.info(f"Auth0 API signup response => {resp}")
            user_data.auth0_id = "auth0|" + resp["_id"]

            # get roles from auth0
            mgmt_auth = Auth0(settings.AUTH0_DOMAIN, settings.AUTH0_MMT_API_TOKEN)
            role_id = mgmt_auth.roles.list()["roles"][0]["id"]
            user_data.role_id = role_id
            user_data.save()

            # assign role to user in auth0
            mgmt_auth.roles.add_users(role_id, users=[user_data.auth0_id])
            return Response(
                {"message": "user registered successful."}, status=status.HTTP_200_OK
            )
        except (Auth0Error, RateLimitError) as e:
            logging.info(f"Auth0 signup error resp => {str(e)}")
            user_data.delete()
            return Response(
                {
                    "message": "something went wrong while creating user please try again.",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user_check = User.objects.get(
                    email__iexact=serializer.validated_data["username"].lower().strip(),
                    is_delete=False,
                    is_active=True,
                    is_superuser=False,
                )
            except User.DoesNotExist:
                response = {
                    "message": "Please enter correct username & password and try again",
                }
                return Response(response, status.HTTP_401_UNAUTHORIZED)
            password = serializer.validated_data["password"]

            # verify user's credentials using auth0
            auth = GetToken(
                settings.AUTH0_DOMAIN,
                settings.AUTH0_CLIENT_ID,
                client_secret=settings.AUTH0_CLIENT_SECRET,
            )
            try:
                # login using auth0
                resp = auth.login(
                    username=serializer.validated_data["username"].lower().strip(),
                    password=password,
                    realm="Username-Password-Authentication",
                )
                logging.info(f"Auth0 login API resp => {resp}")
            except (Auth0Error, RateLimitError) as e:
                logging.info(f"Auth0 login API error resp => {str(e)}")
                return Response(
                    {
                        "message": "Please enter valid username & password and try again",
                        "error": str(e),
                    },
                    status.HTTP_401_UNAUTHORIZED,
                )

            user = authenticate(username=user_check.email, password=password)
            if user and user.is_authenticated:
                login(request, user)
                return Response(
                    {
                        "message": "User logged-in successfully",
                        "user": user.id,
                        "access_token": resp["access_token"],
                        "expires_in": resp["expires_in"],
                        "token_type": resp["token_type"],
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Please enter valid username & password and try again"},
                status.HTTP_401_UNAUTHORIZED,
            )
        else:
            return Response(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
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
