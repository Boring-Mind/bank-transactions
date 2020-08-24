from rest_framework import serializers

from .models import Transactions


class TransactionsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'


class TransactionsReadSerializer(TransactionsPostSerializer):
    sender_id = serializers.IntegerField(
        source='sender_id_id', read_only=True
    )
    receiver_id = serializers.IntegerField(
        source='receiver_id_id', read_only=True
    )
