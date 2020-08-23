from clients.models import Client
from django.db import models
from django.utils.timezone import now
from utils.hashers import generate_unique_sha_512


class Transactions(models.Model):
    # Transaction id is set on save by model itself
    transaction_id = models.CharField(max_length=64, unique=True, blank=True)
    amount = models.FloatField()
    sender_id = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='sender_transaction'
    )
    receiver_id = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='receiver_transaction'
    )
    # Date is set on save by model itself
    date = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        """Make some post-initialization and save object."""
        self.transaction_id = generate_unique_sha_512()
        self.date = now()
        return super().save(*args, **kwargs)
