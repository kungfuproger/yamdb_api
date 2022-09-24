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
    class Meta:
        model = User
        fields = USER_FIELDS
        # lookup_field="username"
        # lookup_url_kwarg = "username"


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = USER_FIELDS
        read_only_fields = ("role",)
