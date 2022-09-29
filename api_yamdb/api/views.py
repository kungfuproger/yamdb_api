from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    decorators, filters, pagination, permissions, status, viewsets,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .mixins import ListCreateDeleteViewSet
from .permissions import (
    AdminOrSuperuserOnly, ReadOnly, SafeOrAuthorOrExceedingRoleOnly,
)
from .serializers import (
    AdminSerializer, CategorySerializer, CommentSerializer, GenreSerializer,
    GetJWTokenSerializer, ProfileSerializer, ReviewSerializer,
    SignUpSerializer, TitleReadSerializer, TitleWriteSerializer,
)
from .utils import code_sender
from reviews.models import Category, Genre, Review, Title
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
    POST
    {
    "email": "string",
    "username": "string"
    }
    """

    def post(self, request):

        try:
            user = User.objects.get(
                username=request.data["username"],
                email=request.data["email"],
            )
            output = request.data
            code_sender(user)
        except (ObjectDoesNotExist, KeyError):
            serializer = SignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            output = serializer.data
            code_sender(user)
        return Response(
            output,
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    Для админа и суперпользователя GET, GET-list, POST, PATCH, DELETE.
    Для авторизованого GET PATCH по url 'me'.
    """

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


class TitleViewSet(viewsets.ModelViewSet):
    """
    Для админа и суперпользователя GET, GET-list, POST, PATCH, DELETE.
    Для анонима GET, GET-list.
    """

    queryset = Title.objects.all()
    serializer_class = TitleReadSerializer
    permission_classes = (AdminOrSuperuserOnly | ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = pagination.PageNumberPagination

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(ListCreateDeleteViewSet):
    """
    Для админа и суперпользователя GET-list, POST, DELETE.
    Для анонима GET-list.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = (AdminOrSuperuserOnly | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenreViewSet(ListCreateDeleteViewSet):
    """
    Для админа и суперпользователя GET-list, POST, DELETE.
    Для анонима GET-list.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    permission_classes = (AdminOrSuperuserOnly | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Для админа и суперпользователя GET, GET-list, POST, PATCH, DELETE.
    Для анонима GET, GET-list.
    Комбинация полей author и title уникальна для каждого Review.
    """

    serializer_class = ReviewSerializer
    permission_classes = (SafeOrAuthorOrExceedingRoleOnly,)
    pagination_class = pagination.PageNumberPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs["title_id"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def create(self, request, *args, **kwargs):
        author = self.request.user
        title = self.get_title()
        if Review.objects.filter(author=author, title=title).exists():
            return Response(
                {"title": "Вы уже оставляли отзыв на это произведение"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Для админа и суперпользователя GET, GET-list, POST, PATCH, DELETE.
    Для анонима GET, GET-list.
    """

    serializer_class = CommentSerializer
    permission_classes = (SafeOrAuthorOrExceedingRoleOnly,)
    pagination_class = pagination.PageNumberPagination

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs["review_id"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()
