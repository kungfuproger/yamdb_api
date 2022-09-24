from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet, GetJWTokenView, SignUpView, TitleViewSet, UserViewSet
)

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="admin_users")
router.register("titles", TitleViewSet, basename="titles")
router.register("categories", CategoryViewSet, basename="categories")

urlpatterns = [
    path("v1/auth/token/", GetJWTokenView.as_view(), name="get_jwtoken"),
    path("v1/auth/signup/", SignUpView.as_view(), name="sign_up"),
    path("v1/", include(router.urls)),
]
