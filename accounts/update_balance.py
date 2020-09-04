from decimal import Decimal

from accounts.models import Account
from currency.exchange_rates import convert_currencies
from django.db.models import Q


class UpdateBalance(object):
    def __init__(self, instance, created=False):
        self.instance = instance
        self.created = created

    def update(self):
        """Update accounts balance after transactions save."""
        if not self.created:
            return

        if (not hasattr(self.instance, 'sender_id')
                or self.instance.sender_id is None):
            # If transaction has only the receiver field
            receiver = Account.objects.get(id=self.instance.receiver_id.id)
            receiver.balance += Decimal(self.instance.amount)
            receiver.save()
            return

        accounts = list(Account.objects.select_related('currency').filter(
            Q(id=self.instance.sender_id.id)
            | Q(id=self.instance.receiver_id.id)
        ))
        
        sender: Account
        receiver: Account

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

        if round(sender.balance - Decimal(self.instance.amount), 4) < 0:
            # If you have not enough money on your balance,
            # you cannot do any outcoming transactions
            # So we revert that transaction.
            self.instance.delete()
            return

        receiver_amount = self.instance.amount
        if sender.currency != receiver.currency:
            receiver_amount = convert_currencies(
                sender.currency,
                receiver.currency,
                self.instance.amount
            )
        
        sender.balance -= Decimal(self.instance.amount)
        receiver.balance += Decimal(receiver_amount)
        Account.objects.bulk_update([sender, receiver], ['balance'])
