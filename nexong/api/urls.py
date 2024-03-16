from django.urls import path, include
from .routers import router_api
from .Authentication.views import (
    RedirectSocial,
    LogoutAndBlacklistRefreshTokenForUserView,
)

urlpatterns = [
    path("", include(router_api.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.social.urls")),
    path(
        "auth/blacklist",
        LogoutAndBlacklistRefreshTokenForUserView.as_view(),
        name="blacklist",
    ),
    path("redirect-social/", RedirectSocial.as_view()),
]
