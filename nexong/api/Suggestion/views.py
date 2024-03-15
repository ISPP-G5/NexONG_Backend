from rest_framework.viewsets import ModelViewSet
from nexong.api.Suggestion.suggestionSerializer import SuggestionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from nexong.models import Suggestion


class SuggestionApiViewSet(ModelViewSet):
    queryset = Suggestion.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = SuggestionSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
