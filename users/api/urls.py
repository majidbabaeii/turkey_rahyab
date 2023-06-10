from django.urls import include, path
from rest_framework import routers

from users.api.views import LoginView, LogoutAPIView, ProfileAPIView, RegisterView

app_name = "auth"
urlpatterns = [
    path("sign-up/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
]
