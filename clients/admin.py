from django.contrib import admin
from .models import Client, Account


@admin.register(Client, Account)
class ClientAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'password',
        'phone_number',
        'passport_number'
    )
