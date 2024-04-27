from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ..permissions import *
from ...models import *
from .lessonSerializer import *


class LessonApiViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = LessonSerializer
    permission_classes = [
        isEducatorGet | isFamilyGet | isVolunteerGet | isEducationCenterGet | isAdmin
    ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        lesson = Lesson.objects.get(pk=pk)
        serializer = self.get_serializer(
            instance,
            data=request.data,
            context={"lesson": lesson, "request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LessonAttendanceApiViewSet(ModelViewSet):
    queryset = LessonAttendance.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = LessonAttendanceSerializer
    permission_classes = [isEducatorGet | isVolunteer | isAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
