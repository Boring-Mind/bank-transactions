from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from currency.models import Currency


class Client(AbstractUser):
	patronymic = models.CharField(max_length=190, blank=True)
	phone_number = models.CharField(max_length=15, unique=True)
	passport_number = models.CharField(max_length=10, unique=True)

	objects = UserManager()
	# instead of Client.objects.create use create_user()
	# That will create hashed password
	# Signature is as follows:
	# create_user(username, password=None, email=None)


class Account(models.Model):
	currency = models.ForeignKey(
		Currency,
		on_delete=models.DO_NOTHING,
		related_name='currency_account'
	)
	client = models.ForeignKey(
		Client,
		on_delete=models.DO_NOTHING,
		related_name='client_account'
	)
