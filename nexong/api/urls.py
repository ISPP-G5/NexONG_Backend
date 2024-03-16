from django.urls import path, include
from .routers import router_api
from .Authentication.views import RedirectSocial

urlpatterns = [
    path("", include(router_api.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.social.urls")),
    path("redirect-social/", RedirectSocial.as_view()),
]
