import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.settings import api_settings

from users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    serializer used for user registration
    """

    password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict):
        user_data = attrs.copy()
        del user_data["password_confirm"]
        user = User(**user_data)

        # get the password from the data
        password = user_data.get("password")

        errors = {}
        try:
            validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if attrs["password"] != attrs["password_confirm"]:
            errors.setdefault(api_settings.NON_FIELD_ERRORS_KEY, [])
            errors[api_settings.NON_FIELD_ERRORS_KEY].append(_("Passwords don't match"))

        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)

    def create(self, validated_data):
        data = validated_data.copy()
        del data["password_confirm"]
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
        ]
