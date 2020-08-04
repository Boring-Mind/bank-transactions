from typing import List

import requests
from django.conf import settings

from .settings import get_currencies


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


def retrieve_rates():
    """Retrieve exchange rates from the server."""
    link = get_link()
    params = get_params()

    response = requests.get(link, params)
    if response.status_code == 200:
        return response.json()['rates']
    else:
        # ToDo: add logging
        return None
