from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ..permissions import *
from ...models import *
from .lessonSerializer import *


class LessonApiViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = LessonSerializer
    permission_classes = [isEducatorPutAndGet | isFamilyGet]

    def update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        old_lesson = Lesson.objects.get(pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if (
            str(old_lesson.educator.pk) != request.data["educator"]
            and request.user.role != "ADMIN"
        ):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonAttendanceApiViewSet(ModelViewSet):
    queryset = LessonAttendance.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = LessonAttendanceSerializer
    permission_classes = [isEducatorPutAndGet | isVolunteerPutAndGet]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
