from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .meetingSerializer import *
from .. import permissions


class MeetingApiViewSet(ModelViewSet):
    queryset = Meeting.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = MeetingSerializer
    permission_classes = [permissions.isAdminOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
