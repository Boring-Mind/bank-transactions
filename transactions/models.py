from decimal import Decimal

from accounts.models import Account
from currency.exchange_rates import convert_currencies
from django.core.validators import MinValueValidator, ValidationError
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from utils.hashers import generate_unique_sha_512


class Transactions(models.Model):
    # Transaction id is set on save by model itself
    transaction_id = models.CharField(max_length=64, unique=True, blank=True)
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
    sender_id = models.ForeignKey(
        Account,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='sender_transaction'
    )
    receiver_id = models.ForeignKey(
        Account,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='receiver_transaction'
    )
    # Date is set on save by model itself
    date = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        """Make some post-initialization and save object."""
        if self.amount < 0.000000000000000:
            raise ValidationError('Transactions amount cannot be negative')
        self.transaction_id = generate_unique_sha_512()
        self.date = now()
        return super().save(*args, **kwargs)


@receiver(post_save, sender=Transactions)
def update_balance(sender, instance, **kwargs):
    """Update accounts balance after transactions save."""
    if not kwargs.get('created'):
        return

    if not hasattr(instance, 'sender_id') or instance.sender_id is None:
        # If transaction has only the receiver field
        receiver = Account.objects.get(id=instance.receiver_id.id)
        receiver.balance += Decimal(instance.amount)
        receiver.save()
        return

    sender = Account.objects.get(id=instance.sender_id.id)
    receiver = Account.objects.get(id=instance.receiver_id.id)

    if round(sender.balance - Decimal(instance.amount), 4) < 0:
        # If you have not enough money on your balance,
        # you cannot do any outcoming transactions
        # So we revert that transaction.
        Transactions.objects.get(id=instance.id).delete()
        return

    receiver_amount = instance.amount
    if sender.currency != receiver.currency:
        receiver_amount = convert_currencies(
            sender.currency.short_name,
            receiver.currency.short_name,
            instance.amount
        )
    
    sender.balance -= Decimal(instance.amount)
    receiver.balance += Decimal(receiver_amount)
    with transaction.atomic():
        sender.save()
        receiver.save()
