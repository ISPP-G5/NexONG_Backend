from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .meetingSerializer import *
from ..permissions import *


class MeetingApiViewSet(ModelViewSet):
    queryset = Meeting.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = MeetingSerializer
    permission_classes = [isPartnerPutAndGet]

    def update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        old_meeting = Meeting.objects.get(pk=pk)
        modified = False

        for field, new_data in serializer.validated_data.items():
            if (
                field not in ("attendees", "url")
                and getattr(old_meeting, field) != new_data
            ):
                modified = True
        if request.user.role != "ADMIN" and modified:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
