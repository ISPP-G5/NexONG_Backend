from django.urls import path, include
from .routers import router_api
from .Authentication.views import UserLoginView

urlpatterns = [
    path("", include(router_api.urls)),
    path("login/", UserLoginView.as_view(), name="user_login"),
]
