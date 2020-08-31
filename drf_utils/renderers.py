import orjson
from rest_framework.renderers import BaseRenderer
from rest_framework.settings import api_settings


class PlainJsonRenderer(BaseRenderer):
    media_type = 'application/json'
    format = 'json'
    compact = api_settings.COMPACT_JSON
    orjson_options = orjson.OPT_UTC_Z | orjson.OPT_OMIT_MICROSECONDS

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Render `data` into JSON, returning a bytestring."""
        if not bool(data):
            return b''

        if not self.compact:
            self.orjson_options |= orjson.OPT_INDENT_2

        ret = orjson.dumps(
            data,
            option=self.orjson_options
        )

        return ret
