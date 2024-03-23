from rest_framework.viewsets import ModelViewSet
from nexong.api.Suggestion.suggestionSerializer import SuggestionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from nexong.models import Suggestion
from ..permissions import *


class SuggestionApiViewSet(ModelViewSet):
    queryset = Suggestion.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = SuggestionSerializer
    permission_classes = [isAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This will automatically set the date field
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
