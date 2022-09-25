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


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели произведения."""

    genre = GenreSerializer(many=True, required=True)
    category = CategorySerializer(required=True)

    class Meta:
        model = Title
        fields = (
            "id", "name", "year", "rating", "description", "genre", "category",
        )

    def create(self, validated_data):
        genres = validated_data.pop("genre")
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            GenresTitles.objects.create(genre=current_genre, title=title)

        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.year = validated_data.get("year", instance.year)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.category = validated_data.get("category", instance.category)

        if "genre" in validated_data:
            genres = validated_data.pop("genre")
            lst = []
            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(**genre)
                lst.append(current_genre)
            instance.genre.set(lst)

        instance.save()
        return instance
