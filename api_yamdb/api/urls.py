from django.urls import include, path

from .views import GetJWTokenView

urlpatterns = [
    path("v1/", include("users.urls")),
    path("v1/auth/token", GetJWTokenView.as_view(), name="get_jwtoken"),
]
