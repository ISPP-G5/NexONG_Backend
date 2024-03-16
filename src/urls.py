from django.contrib import admin
from django.urls import path, include, re_path
from nexong.api.routers import router_api
from nexong import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router_api.urls)),
    re_path(
        r"^NexONG_Backend/files/(?P<path>.*)$", views.serve_file, name="serve_file"
    ),
]
