from django.contrib import admin
from django.urls import path, include, re_path
from nexong.api.routers import router_api
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from nexong import views

schema_view = get_schema_view(
    openapi.Info(
        title="Nexong Docs",
        default_version="v1",
        description="Backend documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="margondia22@alum.us.es"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router_api.urls)),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0)),
    re_path(r"^NexONG_Backend/files/(?P<path>.*)$", views.serve_file, name="serve_file"),
]
