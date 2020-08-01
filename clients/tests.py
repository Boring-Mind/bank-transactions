from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Client


class ModelIntegrationTests(APITestCase):
	def test_password_is_saved_as_hash(self):
		"""Ensure password is stored as correct hash.

		For hashing we use default hasher
		which is listed in Django settings.
		"""
		password = 'SomeP@ssw0rd'
		client = Client.objects.create(
			username='somename',
			password=password,
			phone_number='012345678912345',
			passport_number='0123456789'
		)

		self.assertEquals(Client.objects.count(), 1)

		expected = make_password(password)

		self.assertEquals(client.password, expected)
