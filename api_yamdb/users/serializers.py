from rest_framework import serializers

from .models import User

USER_FIELDS = (
    "username",
    "email",
    "first_name",
    "last_name",
    "bio",
    "role",
)


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
