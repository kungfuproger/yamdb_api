from functools import partial

from rest_framework import (
    decorators, filters, mixins, pagination, permissions, status, viewsets,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import AdminOrSuperuserOnly, OwnProfile
from .serializers import AdminSerializer, ProfileSerializer


class AdminUserViewSet(viewsets.ModelViewSet):
    """ """

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (AdminOrSuperuserOnly, permissions.IsAdminUser)
    lookup_field="username"
    

class ProfileViewSet(viewsets.ModelViewSet):
    """
    Изменить данные своей учетной записи
    Права доступа: Любой авторизованный пользователь
    Поля email и username должны быть уникальными.
    PATCH
    {
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
      }
    """

    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    @decorators.action(methods=("get", "patch"), detail=False, url_path="me")
    def profile(self, request):
        if request.method == "GET":
            serializer = ProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = ProfileSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
