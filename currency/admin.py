from django.contrib import admin

from .models import Currency, ExchangeRate


@admin.register(Currency, ExchangeRate)
class CurrencyAdmin(admin.ModelAdmin):
    pass
