from django.urls import path, include
from .routers import router_api
from .Donation.views import *
from .helpers.volunteerExports import (
    VolunteersExportToCsv,
    VolunteersExportToPdf,
    VolunteersExportToExcel,
    Download_files,
)
from .Student.views import *
from .Authentication.views import (
    LogoutAndBlacklistRefreshTokenForUserView,
    ActivateUserView,
)
from .helpers.partnerExports import (
    PartnersExportToCsv,
    PartnersExportToPdf,
    PartnersExportToExcel,
)
from .PunctualDonationByCard.views import *

urlpatterns = [
    path("", include(router_api.urls)),
    path("export/csv/volunteers", VolunteersExportToCsv, name="export_csv_volunteers"),
    path("export/pdf/volunteers", VolunteersExportToPdf, name="export_pdf_volunteers"),
    path(
        "export/excel/volunteers",
        VolunteersExportToExcel,
        name="export_excel_volunteers",
    ),
    path(
        "export/files/volunteers",
        Download_files,
        name="export_volunteer_files",
    ),
    path("export/csv/donations", DonationsExportToCsv, name="export_csv_all_donations"),
    path("export/pdf/donations", DonationsExportToPdf, name="export_pdf_all_donations"),
    path(
        "export/excel/donations",
        DonationsExportToExcel,
        name="export_excel_all_donations",
    ),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.social.urls")),
    path("auth/activate/", ActivateUserView.as_view(), name="activate-user"),
    path(
        "auth/blacklist/",
        LogoutAndBlacklistRefreshTokenForUserView.as_view(),
        name="blacklist",
    ),
    path("export/csv/students", StudentsExportToCsv, name="export_csv_all_students"),
    path("export/pdf/students", StudentsExportToPdf, name="export_pdf_all_students"),
    path(
        "export/excel/students", StudentsExportToExcel, name="export_excel_all_students"
    ),
    path("auth/", include("djoser.urls.authtoken")),
    path("process-payment", process_payment, name="process_payment"),
    path("payment/success", payment_success, name="payment_success"),
    path("payment/cancel", payment_cancel, name="payment_cancel"),
    path("export/csv/partners", PartnersExportToCsv, name="export_csv_partners"),
    path("export/pdf/partners", PartnersExportToPdf, name="export_pdf_partners"),
    path("export/excel/partners", PartnersExportToExcel, name="export_excel_partners"),

]
