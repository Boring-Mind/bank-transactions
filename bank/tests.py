from django.db import connections
from django.db.utils import OperationalError
from django.test import TestCase


class SmokeTests(TestCase):
    def test_database_is_online(self):
        conn = connections['default']
        try:
            cursor = conn.cursor()
        except OperationalError as err:
            self.fail(f'Db connection was not established\n{err}')
