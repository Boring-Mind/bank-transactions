import logging
from typing import List

import requests
from django.conf import settings
from django.db.models import Q

from .models import Currency
from .settings import get_currencies

err_logger = logging.getLogger('error_logger')


def parse_currencies_to_params(currencies: List[str]) -> str:
    """Convert currencies to the GET params.

    Returns a string with following format:
    'AUD,EUR,GBP,JPY,USD'
    """
    return ','.join(currencies)


def get_params() -> dict:
    cur_list = get_currencies()

    return {
        'app_id': settings.EXCHANGE_APP_ID,
        'symbols': parse_currencies_to_params(cur_list),
        'prettyprint': False
    }


def get_link() -> str:
    return settings.EXCHANGE_LINK


def retrieve_rates() -> dict:
    """Retrieve exchange rates from the server."""
    link = get_link()
    params = get_params()

    try:
        response = requests.get(link, params)
        if response.status_code == 200:
            return response.json()['rates']
        else:
            err_logger.error(
                'Response from Exchange rates API failed.'
                ' Exchange rates was not updated. Try to resend request.'
            )
    except requests.exceptions.RequestException:
        err_logger.exception(
            "Error with sending request to the Exchange rate API",
            exc_info=True
        )
    return None


def update_rates() -> None:
    """Update exchange rates and save them to db.

    Run that task once a day in 00:00 via Celery.
    """
    # ToDo: add await to this
    new_rates = retrieve_rates()

    if not bool(new_rates):
        return

    # ToDo: add await to this
    currencies = Currency.objects.all()

    # Fold into function
    for c in currencies:
        if rate := new_rates.get(c.short_name):
            c.rate = rate

    # ToDo: don't await for the result
    # Make it via asyncio.ensure_future()
    # https://stackoverflow.com/questions/37278647/fire-and-forget-python-async-await
    Currency.objects.bulk_update(currencies, ['rate'])


def convert_currencies(
    c_from: Currency, c_to: Currency, amount: float
) -> float:
    """Convert currency from one to another."""
    return amount * (c_to.rate / c_from.rate)
