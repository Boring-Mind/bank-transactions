from typing import List

from django.conf import settings

CURRENCIES = [
    'USD',
    'EUR',
    'JPY',
    'GBP',
    'AUD',
]


def get_currencies() -> List[str]:
    cur_list = getattr(settings, 'CURRENCIES', CURRENCIES)
    if cur_list is None:
        cur_list = CURRENCIES
    return cur_list
