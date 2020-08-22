from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'username',
            'password',
            'email',
            'patronymic',
            'phone_number',
            'passport_number',
        ]
