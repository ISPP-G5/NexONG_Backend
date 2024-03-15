from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .evaluationSerializer import EvaluationTypeSerializer, StudentEvaluationSerializer
from rest_framework.permissions import AllowAny


class StudentEvaluationApiViewSet(ModelViewSet):
    queryset = StudentEvaluation.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = StudentEvaluationSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EvaluationTypeApiViewSet(ModelViewSet):
    queryset = EvaluationType.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = EvaluationTypeSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
