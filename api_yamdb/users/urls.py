from django.urls import include, path
from rest_framework import routers

from .views import ProfileViewSet, UserViewSet

router = routers.DefaultRouter()
# router.register("users", UserViewSet, basename="users")
router.register("users", ProfileViewSet)


urlpatterns = [
    path("", include(router.urls)),

]
