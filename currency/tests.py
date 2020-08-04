from contextlib import contextmanager
from unittest import mock

from django.conf import settings
from django.test import TestCase

from .exchange_rates import parse_currencies_to_params, retrieve_rates
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
    def requests_get_200(*args, **kwargs) -> mock.MagicMock:
        """Fixture that patches requests.get to the exhange rates API.
        
        Returns status_code == 200 and valid json data.
        """
        response = mock.MagicMock()
        response.status_code = 200
        response.json.return_value = {
            'base': 'USD',
            'disclaimer': (
                'Usage subject to terms:'
                ' https://openexchangerates.org/terms'
            ),
            'license': 'https://openexchangerates.org/license',
            'rates': {
                'AUD': 1.400612,
                'EUR': 0.849127,
                'GBP': 0.764595,
                'JPY': 106.01586364,
                'USD': 1
            },
            'timestamp': 1596524400
        }
        return response

    def requests_get_500(*args, **kwargs) -> mock.MagicMock:
        """Fixture that patches requests.get to the exhange rates API.
        
        Returns status_code == 500.
        """
        response = mock.MagicMock()
        response.status_code = 500
        return response

    def test_parse_currencies_to_params(self):
        expected = 'USD,EUR,JPY,GBP,AUD'
        cur_list = ['USD', 'EUR', 'JPY', 'GBP', 'AUD']
        
        actual = parse_currencies_to_params(cur_list)

        self.assertEqual(actual, expected)

    def test_retrieve_rates_200(self):
        """Unittest for exchange_rates::retrieve_rates function.

        Ensures that valid response is returned.
        Checks branch with response.status_code == 200
        """
        expected = {
            'AUD': 1.400612,
            'EUR': 0.849127,
            'GBP': 0.764595,
            'JPY': 106.01586364,
            'USD': 1
        }

        with mock.patch(
            'requests.get',
            side_effect=__class__.requests_get_200
        ):
            actual = retrieve_rates()

        self.assertEqual(actual, expected)

    def test_retrieve_rates_500(self):
        """Unittest for exchange_rates::retrieve_rates function.

        Ensures that returned value == None.
        Checks branch with response.status_code == 500
        """
        with mock.patch(
            'requests.get',
            side_effect=__class__.requests_get_500
        ):
            actual = retrieve_rates()

        self.assertIsNone(actual)
