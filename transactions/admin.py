from django.contrib import admin
from .models import Transactions


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    pass
