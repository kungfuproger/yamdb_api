from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.status import HTTP_400_BAD_REQUEST

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

USER_FIELDS = (
    "username",
    "email",
    "first_name",
    "last_name",
    "bio",
    "role",
)

TITLE_FIELDS = (
    "id",
    "name",
    "year",
    "rating",
    "description",
    "genre",
    "category",
)


class GetJWTokenSerializer(serializers.ModelSerializer):
    """Сериалайзер получения JWT-токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер самостоятельной подписки."""

    class Meta:
        model = User
        fields = ("email", "username")


class AdminSerializer(serializers.ModelSerializer):
    """
    Сериализатор для супер-пользователя или администратора.
    Доступно изменение всех полей.
    """

    class Meta:
        model = User
        fields = USER_FIELDS


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профайла. Изменение поля 'role' не доступно."""

    class Meta:
        model = User
        fields = USER_FIELDS
        read_only_fields = ("role",)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели категории."""

    class Meta:
        model = Category
        fields = ("name", "slug")
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанра."""

    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведения, только запись."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )

    class Meta:
        model = Title
        fields = TITLE_FIELDS
        read_only_fields = ("id", "rating")


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведения, только чтение."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = TITLE_FIELDS

class CurrentTitleDefault:
    """
    May be applied as a `default=...` value on a serializer field.
    Returns the current user.
    """
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs['title_id']


class ReviewSerializer(serializers.ModelSerializer):
    """Серилизатор отзывов."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True, default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=CurrentTitleDefault())


    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date", "title")

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
