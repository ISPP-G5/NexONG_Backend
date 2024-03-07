from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .donationSerializer import DonationSerializer
from .. import permissions
import csv
from django.http import HttpResponse


class DonationApiViewSet(ModelViewSet):
    queryset = Donation.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = DonationSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


def DonationsExportToCsv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="Datos_Donaciones.csv"'

    # Retrieve data from your model
    queryset = Donation.objects.all()

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(
        ["Cantidad", " Frecuencia", " QuotaExtensionDocument", " Titular", " Fecha"]
    )

    # Write data rows
    for donation in queryset:
        writer.writerow(
            [
                donation.quantity,
                donation.frequency,
                donation.quota_extension_document,
                donation.holder,
                donation.date,
            ]
        )  # Replace field1, field2, etc. with your actual field names

    return response
