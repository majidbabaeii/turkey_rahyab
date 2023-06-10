from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class BadRequest(APIException):
    status_code = 400
    default_detail = _("Bad Request")
    default_code = "bad-request"


class UserNotFound(BadRequest):
    default_detail = _("User not found")
    default_code = "user-not-found"


class LoginInvalid(BadRequest):
    default_detail = _("username or password invalid.")
    default_code = "login-invalid"
