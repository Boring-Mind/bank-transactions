from contextlib import contextmanager
from unittest import mock

from django.conf import settings
from django.test import TestCase

from .exchange_rates import (convert_currencies, parse_currencies_to_params,
                             retrieve_rates, update_rates)
from .models import Currency
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

    def test_update_rates_OK(self):
        """Integration test for exchange_rates::retrieve_rates function.

        Ensures that amount of executed queries is as expected.
        Checks the case when all the received currencies
        matches stored ones and all the values are OK.
        """
        # Create plenty of currencies with outdated rates
        Currency.objects.create(
            short_name="AUD",
            full_name="Australian dollar",
            rate=1.0253
        )
        Currency.objects.create(
            short_name="EUR",
            full_name="Euro",
            rate=0.59683
        )
        Currency.objects.create(
            short_name="GBP",
            full_name="British pound",
            rate=0.86256
        )
        Currency.objects.create(
            short_name="JPY",
            full_name="Japanese yen",
            rate=101.136542
        )
        Currency.objects.create(
            short_name="USD",
            full_name="United states dollar",
            rate=1
        )

        # New rates that would be inserted into db
        rates = {
            'AUD': 1.400612,
            'EUR': 0.849127,
            'GBP': 0.764595,
            'JPY': 106.01586364,
            'USD': 1
        }

        # Check the amount of executed queries
        with self.assertNumQueries(2):
            # Added in order to prevent ambiguous API call
            with mock.patch(
                'currency.exchange_rates.retrieve_rates',
                return_value=rates
            ):
                update_rates()

        currencies = Currency.objects.all()
        updated_rates = {c.short_name: c.rate for c in currencies}
        # Ensure that updated values are correct
        self.assertEqual(rates, updated_rates)

    def test_update_rates_has_more_currencies(self):
        """Integration test for exchange_rates::retrieve_rates function.

        Checks the case when there are more received currencies
        than the stored one. But all the values are OK.
        """
        # Create plenty of currencies with outdated rates
        Currency.objects.create(
            short_name="AUD",
            full_name="Australian dollar",
            rate=1.0253
        )
        Currency.objects.create(
            short_name="EUR",
            full_name="Euro",
            rate=0.59683
        )
        Currency.objects.create(
            short_name="GBP",
            full_name="British pound",
            rate=0.86256
        )
        Currency.objects.create(
            short_name="JPY",
            full_name="Japanese yen",
            rate=101.136542
        )
        Currency.objects.create(
            short_name="USD",
            full_name="United states dollar",
            rate=1
        )

        # New rates that would be inserted into db
        rates = {
            'ALL': 0.698105,
            'AUD': 1.400612,
            'DZD': 8.055390,
            'EUR': 0.849127,
            'GBP': 0.764595,
            'JPY': 106.01586364,
            'XCD': 47.434566,
            'USD': 1
        }

        # Expected result - list should not contain new currencies
        expected = {
            'AUD': 1.400612,
            'EUR': 0.849127,
            'GBP': 0.764595,
            'JPY': 106.01586364,
            'USD': 1
        }

        # Added in order to prevent ambiguous API call
        with mock.patch(
            'currency.exchange_rates.retrieve_rates',
            return_value=rates
        ):
            update_rates()

        currencies = Currency.objects.all()
        updated_rates = {c.short_name: c.rate for c in currencies}
        # Ensure that updated values are correct
        self.assertEqual(expected, updated_rates)

    def test_update_rates_has_less_currencies(self):
        """Integration test for exchange_rates::retrieve_rates function.

        Checks the case when there are less received currencies
        than the stored one. So, some of the values will not update.
        """
        # Create plenty of currencies with outdated rates
        Currency.objects.create(
            short_name="AUD",
            full_name="Australian dollar",
            rate=1.0253
        )
        Currency.objects.create(
            short_name="EUR",
            full_name="Euro",
            rate=0.59683
        )
        Currency.objects.create(
            short_name="GBP",
            full_name="British pound",
            rate=0.86256
        )
        Currency.objects.create(
            short_name="JPY",
            full_name="Japanese yen",
            rate=101.136542
        )
        Currency.objects.create(
            short_name="USD",
            full_name="United states dollar",
            rate=1
        )

        # New rates that would be inserted into db
        rates = {
            'AUD': 1.400612,
            'GBP': 0.764595,
            'USD': 1
        }

        # Expected result - JPY and EUR will not update
        expected = {
            'AUD': 1.400612,
            'EUR': 0.59683,
            'GBP': 0.764595,
            'JPY': 101.136542,
            'USD': 1
        }

        # Added in order to prevent ambiguous API call
        with mock.patch(
            'currency.exchange_rates.retrieve_rates',
            return_value=rates
        ):
            update_rates()

        currencies = Currency.objects.all()
        updated_rates = {c.short_name: c.rate for c in currencies}
        # Ensure that updated values are correct
        self.assertEqual(expected, updated_rates)

    def test_update_rates_received_empty_list(self):
        """Integration test for exchange_rates::retrieve_rates function.

        Checks the case when there was no new values received.
        So, none of the stored values will update.
        """
        # Create plenty of currencies with outdated rates
        Currency.objects.create(
            short_name="AUD",
            full_name="Australian dollar",
            rate=1.0253
        )
        Currency.objects.create(
            short_name="EUR",
            full_name="Euro",
            rate=0.59683
        )
        Currency.objects.create(
            short_name="GBP",
            full_name="British pound",
            rate=0.86256
        )
        Currency.objects.create(
            short_name="JPY",
            full_name="Japanese yen",
            rate=101.136542
        )
        Currency.objects.create(
            short_name="USD",
            full_name="United states dollar",
            rate=1
        )

        # New rates that would be inserted into db
        rates = {}

        # Expected result - no values will be updated
        expected = {
            'AUD': 1.0253,
            'EUR': 0.59683,
            'GBP': 0.86256,
            'JPY': 101.136542,
            'USD': 1
        }

        # Added in order to prevent ambiguous API call
        with mock.patch(
            'currency.exchange_rates.retrieve_rates',
            return_value=rates
        ):
            update_rates()

        currencies = Currency.objects.all()
        updated_rates = {c.short_name: c.rate for c in currencies}
        # Ensure that updated values are correct
        self.assertEqual(expected, updated_rates)

    def test_convert_currencies_OK(self):
        """Integration test for exchange_rates::convert_currencies function.

        Checks the default case - all the currencies are available,
        everything is OK.
        """
        Currency.objects.create(
            short_name="CAD",
            full_name="Canadian dollar",
            rate=1.3146735942,
        )
        Currency.objects.create(
            short_name="HKD",
            full_name="HongKong dollar",
            rate=7.7501885528,
        )

        expected = 5.8951428
        actual = convert_currencies('CAD', 'HKD', 1.0)
        self.assertAlmostEqual(expected, actual)

    def test_convert_currencies_inverse_conversion_OK(self):
        """Integration test for exchange_rates::convert_currencies function.

        Checks inversed order of converse.
        """
        Currency.objects.create(
            short_name="CAD",
            full_name="Canadian dollar",
            rate=1.3146735942,
        )
        Currency.objects.create(
            short_name="HKD",
            full_name="HongKong dollar",
            rate=7.7501885528,
        )

        expected = 0.1696312
        actual = convert_currencies('HKD', 'CAD', 1.0)
        self.assertAlmostEqual(expected, actual)

    def test_convert_currencies_with_custom_amount(self):
        """Integration test for exchange_rates::convert_currencies function.

        Checks custom amount of converse.
        """
        Currency.objects.create(
            short_name="CAD",
            full_name="Canadian dollar",
            rate=1.3146735942,
        )
        Currency.objects.create(
            short_name="HKD",
            full_name="HongKong dollar",
            rate=7.7501885528,
        )

        expected = 17.68607764249819
        actual = convert_currencies('HKD', 'CAD', 104.261953)
        self.assertAlmostEqual(expected, actual)

    def test_convert_currencies_without_any_currencies_in_db(self):
        """Integration test for exchange_rates::convert_currencies function.

        Checks branch where no currency rates was propagated.
        """
        with self.assertRaises(ValueError):
            convert_currencies('HKD', 'CAD', 1.0)
