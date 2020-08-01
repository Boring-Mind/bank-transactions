from rest_framework.test import APITestCase

from .models import Client


class ModelIntegrationTests(APITestCase):
	def test_password_is_saved_as_hash(self):
		"""Ensure password is stored as correct hash.

		For hashing we use Argon2.
		"""
		password = 'SomeP@ssw0rd'
		client = Client.objects.create(
			username='somename',
			password=password,
			phone_number='012345678912345',
			passport_number='0123456789'
		)

		argon_signature = 'argon2$argon2i$v=19$m=512,t=2,'

		self.assertIn(argon_signature, client.password)
