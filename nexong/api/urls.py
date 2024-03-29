from django.urls import path, include
from .routers import router_api
from .Donation.views import *
from .Authentication.views import (
    RedirectSocial,
    LogoutAndBlacklistRefreshTokenForUserView,
    ActivateUserView,
)
from .PunctualDonationByCard.views import *

urlpatterns = [
    path("", include(router_api.urls)),
    path("export/csv/donations", DonationsExportToCsv, name="export_csv_all_donations"),
    path("export/pdf/donations", DonationsExportToPdf, name="export_pdf_all_donations"),
    path(
        "export/excel/donations",
        DonationsExportToExcel,
        name="export_excel_all_donations",
    ),
    path(
        "export/pdf/punctualdonations",
        PunctualDonationsExportToPdf,
        name="export_pdf_all_punctualdonations",
    ),
    path(
        "export/excel/punctualdonations",
        PunctualDonationsExportToExcel,
        name="export_excel_all_punctualdonations",
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
    path("redirect-social/", RedirectSocial.as_view()),
    path("process-payment", process_payment, name="process_payment"),
    path("export/csv/students", StudentsExportToCsv, name="export_csv_all_students"),
    path("export/pdf/students", StudentsExportToPdf, name="export_pdf_all_students"),
    path(
        "export/excel/students", StudentsExportToExcel, name="export_excel_all_students"
    ),
]
