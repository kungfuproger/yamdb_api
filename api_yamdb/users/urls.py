from django.urls import include, path
from rest_framework import routers

from .views import AdminUserViewSet, ProfileViewSet

router = routers.DefaultRouter()
# router.register("users", AdminUserViewSet, basename="admin_users")
router.register("users", ProfileViewSet)
router.register("users", AdminUserViewSet, basename="admin_users")


urlpatterns = [
    path("", include(router.urls)),

]
