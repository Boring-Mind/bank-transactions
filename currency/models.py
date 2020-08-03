from django.db import models
from django.core.validators import MinValueValidator


class Currency(models.Model):
    short_name = models.CharField(max_length=3, unique=True)
    full_name = models.CharField(max_length=25)

class ExchangeRate(models.Model):
    currency_sender = models.ForeignKey(
        'Currency',
        related_name='sender_rate',
        on_delete=models.DO_NOTHING
    )
    currency_receiver = models.ForeignKey(
        'Currency',
        related_name='receiver_rate',
        on_delete=models.DO_NOTHING
    )
    exchange_rate = models.FloatField(validators=[
        MinValueValidator(
            0.0,
            message="Currency exchange rate cannot be less that zero"
        )
    ])