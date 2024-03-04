from rest_framework.viewsets import ModelViewSet
from nexong.api import permissions
from nexong.api.Student.studentSerializer import StudentSerializer
from rest_framework.response import Response
from rest_framework import status

from nexong.models import Student


class StudentApiViewSet(ModelViewSet):
    queryset = Student.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = StudentSerializer
    permission_classes = [permissions.isAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
