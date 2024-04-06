from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .punctualDonationSerializer import PunctualDonationSerializer
from ..permissions import *


class PunctualDonationApiViewSet(ModelViewSet):
    queryset = PunctualDonation.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = PunctualDonationSerializer
    permission_classes = [allowAnyPost | isAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
