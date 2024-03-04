from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .donationSerializer import DonationSerializer
from .. import permissions


class DonationApiViewSet(ModelViewSet):
    queryset = Donation.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = DonationSerializer
    permission_classes = [permissions.isAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
