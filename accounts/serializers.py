from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(
        required=False, max_digits=16, decimal_places=4
    )

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('balance',)
