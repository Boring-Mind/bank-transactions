import json

import pytest
from model_bakery import baker
from rest_framework.renderers import JSONRenderer

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
