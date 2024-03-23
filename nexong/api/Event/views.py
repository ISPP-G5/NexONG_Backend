from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from ..permissions import *
from .eventSerializer import EventSerializer, LessonEventSerializer
from rest_framework.permissions import AllowAny


class EventApiViewSet(ModelViewSet):
    queryset = Event.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = EventSerializer
    permission_classes = [isVolunteerPutAndGet | isPartnerGet | isFamilyPutAndGet]

    def update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        old = Event.objects.get(pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        modified = False
        for field, new_value in serializer.validated_data.items():
            if field not in ("attendees", "volunteers","url") and getattr(old, field) != new_value:
                modified = True
        if request.user.role !="ADMIN" and modified:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role in ("VOLUNTARIO", "VOLUNTARIO_SOCIO") and serializer.validated_data["attendees"] !=list(old.attendees.all()): 
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role == "FAMILIA" and serializer.validated_data["volunteers"] !=list(old.volunteers.all()):
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
    permission_classes = [isVolunteerPutAndGet | isPartnerGet | isFamilyPutAndGet]

    def update(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        old = LessonEvent.objects.get(pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        modified = False

        for field, new_value in serializer.validated_data.items():
            if field not in ("educators","attendees", "volunteers","url") and getattr(old, field) != new_value:
                modified = True
        if request.user.role !="ADMIN" and modified:
                return Response(status=status.HTTP_401_UNAUTHORIZED) 
        
        atendees_mod= "attendees" in serializer.validated_data and serializer.validated_data["attendees"] !=list(old.attendees.all())
        voluntees_mod= "volunteers" in serializer.validated_data and serializer.validated_data["volunteers"] !=list(old.volunteers.all())
        educators_mod= "educators" in serializer.validated_data and serializer.validated_data["educators"] !=list(old.educators.all())
               
        if request.user.role in ("VOLUNTARIO", "VOLUNTARIO_SOCIO") and atendees_mod and educators_mod: 
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role == "FAMILIA" and educators_mod and voluntees_mod:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role == "EDUCADOR" and atendees_mod and voluntees_mod:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
