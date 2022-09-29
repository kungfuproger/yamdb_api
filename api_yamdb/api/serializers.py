from rest_framework import serializers

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


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанра."""

    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"


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
        fields = "__all__"
        read_only_fields = ("id",)


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведения, только чтение."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = TITLE_FIELDS


class ReviewSerializer(serializers.ModelSerializer):
    """Серилизатор отзывов."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
