from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @classmethod
    def get_by_pk(cls, pk: int):
        """
        shortcut for getting user with pk
        """
        return cls.objects.get(pk=pk)

    @classmethod
    def get_by_email(cls, email: str):
        """
        shortcut for getting user with email address
        """
        return cls.objects.get(email=email)
