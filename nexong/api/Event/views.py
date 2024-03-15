from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .eventSerializer import EventSerializer, LessonEventSerializer
from rest_framework.permissions import AllowAny


class EventApiViewSet(ModelViewSet):
    queryset = Event.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonEventApiViewSet(ModelViewSet):
    queryset = LessonEvent.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = LessonEventSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
