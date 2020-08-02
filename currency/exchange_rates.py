from .settings import get_currencies
from typing import List


def parse_currencies_to_params(currencies: List[str]) -> str:
	"""Convert currencies to the GET params."""
	return ','.join(currencies)
