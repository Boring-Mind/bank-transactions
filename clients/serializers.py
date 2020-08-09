from django.db.utils import IntegrityError
from marshmallow import validate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema, fields

from .models import Client


class ClientSerializer(Schema):
    username = fields.String(
        required=True, validate=validate.Regexp(regex=r'[\w@.+_-]{,150}')
    )
    password = fields.String(
        required=True, validate=validate.Length(min=8, max=128)
    )
    email = fields.String(validate=validate.Email())
    patronymic = fields.String(
        validate=validate.Length(max=190)
    )
    phone_number = fields.String(
        required=True, validate=validate.Length(max=15)
    )
    passport_number = fields.String(
        required=True, validate=validate.Length(max=10)
    )

    def create(self, validated_data):
        try:
            client = Client.objects.create_user(**validated_data)
            return client
        except IntegrityError as e:
            field = str(e).split('.')[-1]
            raise ValidationError(
                'Uniqueness check failed for the field ' + field
            )

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class ClientDRFSerializer(serializers.ModelSerializer):
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
