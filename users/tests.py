import contextlib

import pytest
from django.contrib.auth import get_user_model

user_name = "test_user"
user_email = "normal@user.com"
user_email_admin = "admin@user.com"
User = get_user_model()
