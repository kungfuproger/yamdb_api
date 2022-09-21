from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import GetJWTokenSerializer
from users.models import User


class GetJWTokenView(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    Только POST запросы. Доступно без токена.
        Принимает:
        {
        "username": "string",
        "confirmation_code": "string"
        }
        Возвращает:
        {
        "token": "string"
        }
    """

    def post(self, request):
        serializer = GetJWTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(
                username=data["username"],
                confirmation_code=data["confirmation_code"],
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "username": "This pair does not exist!",
                    "confirmation_code": "This pair does not exist!",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        token = AccessToken.for_user(user)
        return Response(
            {
                "token": str(token),
            },
            status=status.HTTP_201_CREATED,
        )
