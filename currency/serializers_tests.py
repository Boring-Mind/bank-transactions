import pytest

from .models import Currency
from .serializers import CurrencyReadSerializer


@pytest.mark.django_db
def test_currency_read_serializer_correct_serialization():
    Currency.objects.bulk_create([
        Currency(
            short_name="AUD",
            full_name="Australian dollar",
            rate=1.0253
        ),
        Currency(
            short_name="EUR",
            full_name="Euro",
            rate=0.59683
        )
    ])
    queryset = Currency.objects.all()
    expected = {"AUD": 1.0253, "EUR": 0.59683}

    actual = CurrencyReadSerializer.serialize_data(queryset)

    assert expected == actual
