from django.contrib.auth import authenticate
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response

from core.utils.drf import APIViewWithContext
from users.api.exceptions import LoginInvalid
from users.api.serializers.login_serializer import LoginSerializer
from users.api.serializers.register_serializers import RegisterUserSerializer
from users.api.serializers.user_serializers import UserSerializer


class RegisterView(APIViewWithContext):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserSerializer
    response_serializer_class = UserSerializer

    def post(self, request: Request) -> Response:
        """
        Register new user.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        kwargs = {}

        with transaction.atomic():
            user = serializer.save(**kwargs)

        response_serializer = self.response_serializer_class(
            instance=user,
            context=self.get_serializer_context(),
        )
        user_data = response_serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(APIViewWithContext):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """
        Log in the user via given login and password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data.get("username")
        password = serializer.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"detail": _("Login successful"), "token": token.key})
        else:
            raise LoginInvalid()


class LogoutAPIView(APIViewWithContext):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Logout user and delete token.
        """
        # Get the user's token
        token = request.auth
        if token:
            # Delete the token
            token.delete()

        # Provide a response
        return Response({"success": "User logged out"})


class ProfileAPIView(APIViewWithContext):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request: Request) -> Response:
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)
