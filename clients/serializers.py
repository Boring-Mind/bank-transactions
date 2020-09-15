from django.db.models import Q
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
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ClientWriteSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField(required=False)
    patronymic = serializers.CharField(max_length=190, required=False)
    phone_number = serializers.CharField(max_length=15)
    passport_number = serializers.CharField(max_length=10)

    def check_uniqueness(self, data):
        """Check the uniqueness of all the unique fields in one query."""
        clients = list(Client.objects.filter(
            Q(username=data['username'])
            | Q(phone_number=data['phone_number'])
            | Q(passport_number=data['passport_number'])
        ))

        if len(clients) > 0:
            raise serializers.ValidationError(
                {"message": "Uniqueness check is failed"}
            )

    def validate(self, data):
        self.check_uniqueness(data)
        return data

    def create(self, validated_data):
        return Client.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
