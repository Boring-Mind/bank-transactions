from clients.models import Client
from currency.models import Currency
from django.core.validators import MinValueValidator
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
    balance = models.DecimalField(
        default=0.0,
        max_digits=16,
        decimal_places=4,
        validators=[MinValueValidator]
    )
