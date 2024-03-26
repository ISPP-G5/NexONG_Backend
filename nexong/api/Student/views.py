from rest_framework.viewsets import ModelViewSet
from nexong.api.Student.studentSerializer import (
    StudentSerializer,
    QuarterMarksSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from nexong.models import Student, QuarterMarks, STATUS, CURRENT_EDUCATION_YEAR
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
from nexong.models import Student, QuarterMarks
from ..permissions import *
from nexong.api.helpers.permissionValidators import *
from rest_framework.permissions import AllowAny
from nexong.models import Student, QuarterMarks


class StudentApiViewSet(ModelViewSet):
    queryset = Student.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = StudentSerializer
    permission_classes = [isFamily | isEducatorGet]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create_or_update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if only_modified_if_same_role(
            request.user.family, serializer.validated_data["family"], request.user.role
        ):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()
        return Response(serializer.data)


class QuarterMarksApiViewSet(ModelViewSet):
    queryset = QuarterMarks.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = QuarterMarksSerializer
    permission_classes = [isFamily | isEducatorGet]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
