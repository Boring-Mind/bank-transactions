from contextlib import contextmanager

from django.conf import settings
from django.test import TestCase

from .exchange_rates import parse_currencies_to_params
from .settings import get_currencies


@contextmanager
def custom_currencies():
    """Save previous CURRENCIES value and restore it after operations."""
    # Save original CURRENCIES value
    global_currencies = getattr(settings, 'CURRENCIES', None)
    yield None
    # Restore CURRENCIES value
    settings.CURRENCIES = global_currencies


class SettingsTests(TestCase):
    def test_get_default_currencies(self):
        """Test settings::get_currencies() without global SURRENCIES var."""
        expected = ['USD', 'EUR', 'JPY', 'GBP', 'AUD']

        with custom_currencies():
            settings.CURRENCIES = None
            actual = get_currencies()

        self.assertEqual(actual, expected)

    def test_get_custom_currencies(self):
        """Test settings::get_currencies() with setted SURRENCIES value.

        Expected value must differ from default currencies list,
        which is set in currency::settings.
        """
        expected = ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'AED']

        with custom_currencies():
            settings.CURRENCIES = expected
            actual = get_currencies()

        self.assertEqual(actual, expected)


class ExchangeRatesTests(TestCase):
    def test_parse_currencies_to_params(self):
        expected = 'USD,EUR,JPY,GBP,AUD'
        cur_list = ['USD', 'EUR', 'JPY', 'GBP', 'AUD']
        
        actual = parse_currencies_to_params(cur_list)

        self.assertEqual(actual, expected)
