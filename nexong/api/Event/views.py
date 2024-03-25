from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from ..permissions import *
from .eventSerializer import EventSerializer, LessonEventSerializer
from nexong.api.helpers.permissionValidators import *


class EventApiViewSet(ModelViewSet):
    queryset = Event.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = EventSerializer
    permission_classes = [isVolunteerPutAndGet | isPartnerGet | isFamilyPutAndGet]

    def update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        old_event = Event.objects.get(pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if (
            validate_except_fields(
                request.user.role,
                serializer.validated_data.items(),
                old_event,
                ("attendees", "volunteers", "url"),
            )
            or modified_not_allowed_for_roles(
                request.user.role,
                ("VOLUNTARIO", "VOLUNTARIO_SOCIO"),
                serializer.validated_data["attendees"]
                != list(old_event.attendees.all()),
            )
            or modified_not_allowed_for_roles(
                request.user.role,
                ("FAMILIA"),
                serializer.validated_data["volunteers"]
                != list(old_event.volunteers.all()),
            )
        ):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonEventApiViewSet(ModelViewSet):
    queryset = LessonEvent.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = LessonEventSerializer
    permission_classes = [
        isVolunteerPutAndGet | isPartnerGet | isFamilyGet | isEducatorPutAndGet
    ]

    def update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        old_lessonEvent = LessonEvent.objects.get(pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        atendees_mod = (
            "attendees" in serializer.validated_data
            and serializer.validated_data["attendees"]
            != list(old_lessonEvent.attendees.all())
        )
        voluntees_mod = (
            "volunteers" in serializer.validated_data
            and serializer.validated_data["volunteers"]
            != list(old_lessonEvent.volunteers.all())
        )
        educators_mod = (
            "educators" in serializer.validated_data
            and serializer.validated_data["educators"]
            != list(old_lessonEvent.educators.all())
        )
        if (
            validate_except_fields(
                request.user.role,
                serializer.validated_data.items(),
                old_lessonEvent,
                ("educators", "attendees", "volunteers", "url"),
            )
            or modified_not_allowed_for_roles(
                request.user.role,
                ("VOLUNTARIO", "VOLUNTARIO_SOCIO"),
                atendees_mod and educators_mod,
            )
            or modified_not_allowed_for_roles(
                request.user.role, ("EDUCADOR"), voluntees_mod
            )
        ):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
