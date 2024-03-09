from django.urls import path, include
from .routers import router_api
from .Donation.views import *
urlpatterns = [
    path("", include(router_api.urls)),
    path("export/csv/donations", DonationsExportToCsv, name="export_csv_all_donations"),
    path("export/pdf/donations", DonationsExportToPdf, name="export_pdf_all_donations"),
    path("export/excel/donations", DonationsExportToExcel, name="export_excel_all_donations"),
]