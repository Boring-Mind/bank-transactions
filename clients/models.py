from currency.models import Currency
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class ClientManager(UserManager):
    def create(self, *args, **kwargs):
        """Override default create method.

        Create_user method is needed
        for proper password hashing
        and field validation.
        """
        return super().create_user(*args, **kwargs)


class Client(AbstractUser):
    patronymic = models.CharField(max_length=190, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    passport_number = models.CharField(max_length=10, unique=True)

    objects = ClientManager()


class Account(models.Model):
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='currency_account'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='client_account'
    )
