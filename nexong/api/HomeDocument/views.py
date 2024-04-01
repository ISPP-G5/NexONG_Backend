from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .homeDocumentSerializer import HomeDocumentSerializer
from ..permissions import *


class HomeDocumentApiViewSet(ModelViewSet):
    queryset = HomeDocument.objects.all()
    http_method_names = ["get", "post", "put", "delete", "patch"]
    serializer_class = HomeDocumentSerializer
    permission_classes = [isAuthenticated | isAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
