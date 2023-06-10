from rest_framework import serializers


class LoginSerializer(
    serializers.Serializer
):  # noqa: E501 pylint: disable=abstract-method
    """
    serializer used for user login.
    """

    username = serializers.CharField()
    password = serializers.CharField()
