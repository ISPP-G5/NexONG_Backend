from rest_framework.viewsets import ModelViewSet
from nexong.api.Student.studentSerializer import (
    StudentSerializer,
    QuarterMarksSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from nexong.models import Student, QuarterMarks
from ..permissions import *
from nexong.api.helpers.permissionValidators import *


class StudentApiViewSet(ModelViewSet):
    queryset = Student.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = StudentSerializer
    permission_classes = [isFamily | isEducatorGet]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if only_modified_if_same_role(
            request.user.family, serializer.validated_data["family"], request.user.role
        ):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if only_modified_if_same_role(
            request.user.family, serializer.validated_data["family"], request.user.role
        ):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuarterMarksApiViewSet(ModelViewSet):
    queryset = QuarterMarks.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = QuarterMarksSerializer
    permission_classes = [isFamily | isEducatorGet]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
