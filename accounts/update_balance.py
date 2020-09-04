from decimal import Decimal

from accounts.models import Account
from currency.exchange_rates import convert_currencies
from django.db.models import Q


class UpdateBalance(object):
    def __init__(self, instance, created=False):
        self.instance = instance
        self.created = bool(created)

    def retrieve_accounts(self) -> (Account, Account):
        """Retrieve receiver and sender accounts from the db.

        Raises IndexError when query returned more or less than two accounts.
        """
        sender: Account
        receiver: Account

        accounts = list(Account.objects.select_related('currency').filter(
            Q(id=self.instance.sender_id.id)
            | Q(id=self.instance.receiver_id.id)
        ))

        try:
            if accounts[0].id == self.instance.sender_id.id:
                sender = accounts[0]
                receiver = accounts[1]
            else:
                receiver = accounts[0]
                sender = accounts[1]
        except IndexError:
            raise IndexError(
                f"Database returned {len(accounts)} objects instead of 2"
            )
        return (sender, receiver)

    def transaction_has_not_sender(self) -> bool:
        """Return True when transaction has not sender field."""
        return (not hasattr(self.instance, 'sender_id')
                or self.instance.sender_id is None)

    def deposit_to_the_receiver(self):
        """Deposit transactions amount to the receivers account."""
        receiver = Account.objects.get(id=self.instance.receiver_id.id)
        receiver.balance += Decimal(self.instance.amount)
        return receiver.save()

    def not_enough_money(self, account: Account) -> bool:
        """Return True when there are not enough money in the account."""
        return round(account.balance - Decimal(self.instance.amount), 4) < 0

    def transaction_failed(self) -> bool:
        """Return True if transaction wasn't saved."""
        return not self.created

    def rollback_transaction(self):
        """Rollback transaction if needed."""
        return self.instance.delete()

    def get_receiver_amount(self, sender: Account, receiver: Account) -> float:
        """Get amount of money that would be sent to the receivers account."""
        receiver_amount = self.instance.amount
        if sender.currency != receiver.currency:
            receiver_amount = convert_currencies(
                sender.currency,
                receiver.currency,
                self.instance.amount
            )
        return receiver_amount

    def update(self) -> None:
        """Update accounts balance after transactions save."""
        if self.transaction_failed():
            return

        if self.transaction_has_not_sender():
            self.deposit_to_the_receiver()
            return

        sender, receiver = self.retrieve_accounts()

        if self.not_enough_money(sender):
            # If you have not enough money on your balance,
            # you cannot do any outcoming transactions
            # So we revert that transaction.
            self.rollback_transaction()
            return

        receiver_amount = self.get_receiver_amount(sender, receiver)
        
        sender.balance -= Decimal(self.instance.amount)
        receiver.balance += Decimal(receiver_amount)
        Account.objects.bulk_update([sender, receiver], ['balance'])
