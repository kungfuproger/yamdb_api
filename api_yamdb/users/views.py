from rest_framework import (
    decorators, mixins, pagination, permissions, status, viewsets,
)
from rest_framework.response import Response

from .models import User
from .permissions import AdminOrSuperuserOnly
from .serializers import AdminSerializer, ProfileSerializer


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (AdminOrSuperuserOnly,)
    lookup_field = "username"
    pagination_class = pagination.PageNumberPagination
    search_fields = ("username",)

    @decorators.action(
        methods=("get", "patch"),
        detail=False,
        url_path="me",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def profile(self, request):
        if request.method == "GET":
            serializer = ProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = ProfileSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
