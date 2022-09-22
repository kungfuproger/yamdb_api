from django.urls import include, path

from .views import GetJWTokenView, SignUpView

urlpatterns = [
    path("v1/", include("users.urls")),
    path("v1/auth/token/", GetJWTokenView.as_view(), name="get_jwtoken"),
    path("v1/auth/signup/", SignUpView.as_view(), name="sign_up"),
]
