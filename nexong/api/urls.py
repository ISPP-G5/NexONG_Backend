from django.urls import path, include
from .routers import router_api
from .Donation.views import *
from .Authentication.views import (
    RedirectSocial,
    LogoutAndBlacklistRefreshTokenForUserView,
    ActivateUserView,
)

urlpatterns = [
    path("", include(router_api.urls)),
    path("export/csv/donations", DonationsExportToCsv, name="export_csv_all_donations"),
    path("export/pdf/donations", DonationsExportToPdf, name="export_pdf_all_donations"),
    path(
        "export/excel/donations",
        DonationsExportToExcel,
        name="export_excel_all_donations",
    ),
    path("auth/", include("djoser.urls")),
    #path("activate/<str:uid>/<str:token>", ActivateUserView.as_view(), name="activate-user"),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.social.urls")),
    path("auth/activate/", ActivateUserView.as_view(), name="activate-user"),
    path(
        "auth/blacklist/",
        LogoutAndBlacklistRefreshTokenForUserView.as_view(),
        name="blacklist",
    ),
    path("redirect-social/", RedirectSocial.as_view()),
]
