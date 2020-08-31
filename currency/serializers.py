class CurrencyReadSerializer(object):
    """Read-only plain currency serializer.

    Returns raw json with current rates in the format:
    {"short_name":rate}
    """
    @staticmethod
    def serialize_data(queryset) -> str:
        return {entry.short_name: entry.rate for entry in queryset}
