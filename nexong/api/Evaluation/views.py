from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .evaluationSerializer import EvaluationTypeSerializer, StudentEvaluationSerializer
from ..permissions import *


class StudentEvaluationApiViewSet(ModelViewSet):
    queryset = StudentEvaluation.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = StudentEvaluationSerializer
    permission_classes = [isEducator | isFamilyGet]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EvaluationTypeApiViewSet(ModelViewSet):
    queryset = EvaluationType.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = EvaluationTypeSerializer
    permission_classes = [isEducator]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        eval_lesson = serializer.validated_data["lesson"]
        if (
            eval_lesson.educator != request.user.educator
            and request.user.role != "ADMIN"
        ):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
