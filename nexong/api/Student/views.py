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
    writer.writerow([
        smart_str(u"Nombre"),
        smart_str(u"Apellido"),
        smart_str(u"Curso Actual"),
        smart_str(u"Nacionalidad"),
        smart_str(u"Fecha de Nacimiento"),
        smart_str(u"Estudiante de Mañana"),
        smart_str(u"Estado"),
        smart_str(u"Centro Educativo"),
        smart_str(u"Familia")
    ])

    # Retrieve data from your model
    queryset = Student.objects.all()

    # Write data rows
    for student in queryset:
        writer.writerow([
            smart_str(student.name),
            smart_str(student.surname),
            smart_str(student.current_education_year),
            smart_str(student.nationality),
            smart_str(student.birthdate),
            smart_str(student.is_morning_student),
            smart_str(student.status),
            smart_str(student.education_center),
            smart_str(student.family)
        ])

    return response
