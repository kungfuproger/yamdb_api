from rest_framework import serializers

from reviews.models import Category, Genre, Title, GenresTitles
from users.models import User


USER_FIELDS = (
    "username",
    "email",
    "first_name",
    "last_name",
    "bio",
    "role",
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
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанра."""

    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведения."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )

    class Meta:
        model = Title
        fields = (
            "id", "name", "year", "rating", "description", "genre", "category",
        )
        read_only_fields = ("id", "rating")


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведения."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            "id", "name", "year", "rating", "description", "genre",
            "category",
        )
