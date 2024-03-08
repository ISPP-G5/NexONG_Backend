from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .donationSerializer import DonationSerializer
from .. import permissions
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas

class DonationApiViewSet(ModelViewSet):
    queryset = Donation.objects.all()
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = DonationSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def DonationsExportToCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Datos_Donaciones.csv"'

    # Retrieve data from your model
    queryset = Donation.objects.all()

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Cantidad', ' Frecuencia', ' QuotaExtensionDocument', ' Titular', ' Fecha'])

    # Write data rows
    for donation in queryset:
        writer.writerow([donation.quantity, donation.frequency, donation.quota_extension_document, donation.holder, donation.date])  # Replace field1, field2, etc. with your actual field names

    return response

def DonationsExportToPdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Datos_Donaciones.pdf"'
    # Create a PDF document
    c = canvas.Canvas(response)

    # Retrieve data from your model
    queryset = Donation.objects.all()

    # Set the starting y coordinate for drawing the text
    y_coordinate = 750

    # Write data rows
    for donation in queryset:
        data_row = [
            'Cantidad: ' + str(donation.quantity), 
            'Frecuencia: ' + str(donation.frequency), 
            'Documento: '+ str(donation.quota_extension_document), 
            'Titular: '+ str(donation.holder), 
            'Fecha: ' + str(donation.date),
            '---------------------------------------'
        ]
        for data in data_row:
            c.drawString(100, y_coordinate, data)
            y_coordinate -= 20  # Move to the next line

    # Close the PDF document
    c.save()

    return response
