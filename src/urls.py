from django.contrib import admin
from django.urls import path, include, re_path
from nexong.api.urls import urlpatterns as api_urls
from nexong import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
    re_path(
        r"^NexONG_Backend/files/(?P<path>.*)$", views.serve_file, name="serve_file"
    ),
]
