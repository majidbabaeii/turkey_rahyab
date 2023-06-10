from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    user profile Serializer
    """

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "is_staff",
            "date_joined",
        ]

        read_only_fields = [
            "username",
            "is_staff",
            "date_joined",
        ]
