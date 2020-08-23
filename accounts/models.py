from clients.models import Client
from currency.models import Currency
from django.db import models


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
