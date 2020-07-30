from django.db import models
from clients.models import Client
from currency.models import Currency


class Transactions(models.Model):
	transaction_id = models.CharField(max_length=64, unique=True)
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
