import requests
from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .authSerializer import *
from rest_framework_simplejwt.tokens import RefreshToken


def process_instance(serializer_class, instance, data):
    serializer = serializer_class(instance, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserApiViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = UserSerializer
    queryset = User.objects.all()


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
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = PartnerSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class VolunteerApiViewSet(ModelViewSet):
    queryset = Volunteer.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
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


class RedirectSocial(View):
    def get(self, request, *args, **kwargs):
        code, state = str(request.GET["code"]), str(request.GET["state"])
        json_obj = {"code": code, "state": state}
        return JsonResponse(json_obj)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    # permission_classes = (permissions.AllowAny,)
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

    def post(self, request):
        access_token = request.headers.get("Authorization")
        url = "http://localhost:8000/api/auth/users/me"  # Actualiza con la URL de tu aplicación
        headers = {"Authorization": access_token}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            try:
                email = response.json()["email"]
                user = User.objects.get(email=email)
                if not user.is_enabled and not user.id_number:
                    user.is_enabled = True
                    user.save()
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=response.status_code)
