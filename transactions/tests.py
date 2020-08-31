import json

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from utils.fixtures import api_client

from .models import Transactions
from .serializers import TransactionsReadSerializer


@pytest.fixture
def transaction_obj():
    return baker.make(
        Transactions,
        id=4,
        amount=10411.326,
        sender_id__id=2,
        receiver_id__id=3
    )


@pytest.fixture
def superuser():
    return baker.make('clients.Client', is_staff=True)


@pytest.mark.django_db
def test_transactionsreadserializer_returns_valid_json(transaction_obj):
    """Check that serializer serializes related values correctly.

    The main goal of that test is to make sure that sender_id
    and receiver_id are serialized correctly.
    """
    serializer = TransactionsReadSerializer(transaction_obj)

    actual = JSONRenderer().render(serializer.data)
    actual = json.loads(actual)

    assert actual['id'] == 4
    assert actual['amount'] == 10411.326
    assert actual['sender_id'] == 2
    assert actual['receiver_id'] == 3


# Unfinished test for TransactionsIncomingView
# @pytest.mark.django_db
# def test_transactions_incoming_view_filters_transactions(superuser, api_client):
#     tr1 = baker.make('transactions.Transactions', id=1, sender_id__id=1, receiver_id__id=2)
#     tr2 = baker.make('transactions.Transactions', id=2, sender_id__id=1, receiver_id__id=2)
#     tr3 = baker.make('transactions.Transactions', id=3, sender_id__id=2, receiver_id__id=1)

#     url = (
#         reverse('transactions') +
#         '?page=2&incoming=False&acc_id=3'
#     )
#     token = RefreshToken.for_user(superuser)

#     api_client.credentials(
#         HTTP_AUTHORIZATION=f'Bearer {token.access_token}'
#     )
#     response = api_client.get(url, format='json')
#     assert 2 == 3
