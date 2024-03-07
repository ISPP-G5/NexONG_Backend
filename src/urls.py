from django.contrib import admin
from django.urls import path, include
from nexong.api.routers import router_api
from nexong.api.Donation.views import *

urlpatterns = [path("admin/", admin.site.urls), path("api/", include(router_api.urls)), path("api/donation/export", DonationsExportToCsv, name="export-donation-to-csv")]
