from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import GetJWTokenSerializer, SignUpSerializer
from .utils import code_generator
from users.models import User

CODE_EMAIL = "confirmation_code@yamdb.yandex"


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
            user = User.objects.get(username=data["username"])
        except ObjectDoesNotExist:
            return Response(
                {
                    "username": "This username does not exist!",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if user.confirmation_code != data["confirmation_code"]:
            return Response(
                {"confirmation_code": "Wrong confirmation_code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = AccessToken.for_user(user)
        return Response(
            {
                "token": str(token),
            },
            status=status.HTTP_201_CREATED,
        )


class SignUpView(APIView):
    """
    Получить код подтверждения на переданный email.
    Права доступа: Доступно без токена.
    Использовать имя 'me' в качестве username запрещено.
    Поля email и username должны быть уникальными.
    {
    "email": "string",
    "username": "string"
    }
    """

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = code_generator(10)
        # создаем нового юзера
        user = serializer.save()
        user.confirmation_code = code
        user.save()

        send_mail(
            "Api_Yamdb confirmation_code",
            f"confirmation_code: {code}",
            CODE_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
