from accounts.models import Account
from accounts.update_balance import UpdateBalance
from django.core.validators import MinValueValidator, ValidationError
from django.db import models
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
    UpdateBalance(instance, created=kwargs.get('created')).update()
