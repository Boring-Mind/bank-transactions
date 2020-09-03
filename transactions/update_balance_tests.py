from decimal import Decimal

import pytest
from accounts.models import Account
from clients.models import Client
from currency.models import Currency
from django.core.validators import ValidationError

from .models import Transactions


def get_client():
    """Fixture that returns one client object."""
    return Client.objects.create(
        username="some_name",
        password="S0m3_passw0rd",
        passport_number="1131230",
        phone_number="113131035"
    )


def get_two_clients():
    """Fixture that returns two clients."""
    client1 = Client.objects.create(
        username="some_name",
        password="S0m3_passw0rd",
        passport_number="1131230",
        phone_number="113131035"
    )
    client2 = Client.objects.create(
        username="some_name2",
        password="S0m3_passw0rd",
        passport_number="11312302",
        phone_number="11313152"
    )
    return (client1, client2)


@pytest.mark.django_db
def test_transaction_in_one_currency():
    """Check that account balances was changed after correct transaction.

    Integration test that tests sender and receiver balances changing
    after the correct transactions save. Operations are made in one currency.
    """
    client1, client2 = get_two_clients()
    currency = Currency.objects.create(
        short_name="USD", full_name="United States dollar", rate=0
    )
    sender = Account.objects.create(
        currency=currency,
        client=client1,
        balance=Decimal("1000")
    )
    receiver = Account.objects.create(
        currency=currency,
        client=client2
    )

    expected_sender_balance = Decimal("500")
    expected_receiver_balance = Decimal("500")

    Transactions.objects.create(
        amount=500.0,
        sender_id=sender,
        receiver_id=receiver
    )

    sender.refresh_from_db(fields=('balance',))
    receiver.refresh_from_db(fields=('balance',))

    assert expected_sender_balance == sender.balance
    assert expected_receiver_balance == receiver.balance


@pytest.mark.django_db
def test_transaction_in_two_currencies():
    """Check that account balances was changed after correct transaction.

    Integration test that tests sender and receiver balances changing
    after the correct transactions save. Operations are made in two currencies.
    """
    client1, client2 = get_two_clients()
    currency1 = Currency.objects.create(
        short_name="CAD", full_name="Canadian dollar", rate=1.3014098607
    )
    currency2 = Currency.objects.create(
        short_name="HKD", full_name="Hong Kong dollar", rate=7.7500625678
    )
    sender = Account.objects.create(
        currency=currency1,
        client=client1,
        balance=Decimal("1000")
    )
    receiver = Account.objects.create(
        currency=currency2,
        client=client2
    )

    expected_sender_balance = Decimal("900.0")
    expected_receiver_balance = Decimal("595.5128205061709")

    Transactions.objects.create(
        amount=100.0,
        sender_id=sender,
        receiver_id=receiver
    )

    sender.refresh_from_db(fields=('balance',))
    receiver.refresh_from_db(fields=('balance',))

    assert round(expected_sender_balance, 4) == round(sender.balance, 4)
    assert round(expected_receiver_balance, 4) == round(receiver.balance, 4)


@pytest.mark.django_db
def test_transaction_when_sender_has_not_enough_money():
    """Check the case - sender hasn't enough money to proceed transaction.

    Expected behaviour - transaction will rool back
    and payment will not proceed.
    """
    client1, client2 = get_two_clients()
    currency = Currency.objects.create(
        short_name="USD", full_name="United States dollar", rate=0
    )
    sender = Account.objects.create(
        currency=currency,
        client=client1,
        balance=Decimal("999")
    )
    receiver = Account.objects.create(
        currency=currency,
        client=client2
    )

    expected_sender_balance = Decimal("999")
    expected_receiver_balance = Decimal("0")

    Transactions.objects.create(
        amount=1000.0,
        sender_id=sender,
        receiver_id=receiver
    )

    sender.refresh_from_db(fields=('balance',))
    receiver.refresh_from_db(fields=('balance',))

    assert expected_sender_balance == sender.balance
    assert expected_receiver_balance == receiver.balance

    # Assert that transaction was deleted
    assert Transactions.objects.count() == 0


@pytest.mark.django_db
def test_deposit_transaction_with_no_sender():
    """Check the case of deposit transaction - only receiver field is set.

    Check that valid transaction leads to receivers balance increase.
    """
    client1 = get_client()
    currency = Currency.objects.create(
        short_name="USD", full_name="United States dollar", rate=0
    )
    receiver = Account.objects.create(
        currency=currency,
        client=client1
    )

    expected_receiver_balance = Decimal("500")

    Transactions.objects.create(
        amount=500.0,
        receiver_id=receiver,
        sender_id=None
    )

    receiver.refresh_from_db(fields=('balance',))

    assert expected_receiver_balance == receiver.balance


@pytest.mark.django_db
def test_transaction_was_not_successful():
    """Check the case - transaction wasn't saved.

    Expected behaviour - transaction will rool back
    and payment will not proceed.
    """
    client1 = get_client()
    currency = Currency.objects.create(
        short_name="USD", full_name="United States dollar", rate=0
    )
    receiver = Account.objects.create(
        currency=currency,
        client=client1
    )

    expected_receiver_balance = Decimal()

    with pytest.raises(ValidationError):
        Transactions.objects.create(
            amount=-500.0,
            receiver_id=receiver,
            sender_id=None
        )

    receiver.refresh_from_db(fields=('balance',))

    assert expected_receiver_balance == receiver.balance
