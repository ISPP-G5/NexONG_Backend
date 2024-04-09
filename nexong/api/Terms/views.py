from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ..permissions import *
from ...models import *
from .termsSerializer import *


class TermsApiViewSet(ModelViewSet):
    queryset = Terms.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = TermsSerializer
    permission_classes = [allowAnyGet | isAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
