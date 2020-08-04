from django.core.validators import MinValueValidator
from django.db import models


class Currency(models.Model):
    short_name = models.CharField(max_length=3, unique=True)
    full_name = models.CharField(max_length=25)
    rate = models.FloatField(validators=[
        MinValueValidator(
            0.0,
            message="Currency exchange rate cannot be less that zero"
        )
    ])
