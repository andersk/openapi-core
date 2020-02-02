import pytest

from openapi_core.schema.media_types.exceptions import InvalidMediaTypeValue
from openapi_core.schema.media_types.models import MediaType
from openapi_core.schema.schemas.models import Schema
from openapi_core.unmarshalling.schemas.formatters import Formatter


class TestMediaTypeCast(object):

    def test_empty(self):
        media_type = MediaType('application/json')
        value = ''

        result = media_type.cast(value)

        assert result == value


class TestParameterUnmarshal(object):

    def test_empty(self):
        media_type = MediaType('application/json')
        value = ''

        result = media_type.unmarshal(value)

        assert result == value

    def test_schema_type_invalid(self):
        schema = Schema('integer', _source={'type': 'integer'})
        media_type = MediaType('application/json', schema=schema)
        value = 'test'

        with pytest.raises(InvalidMediaTypeValue):
            media_type.unmarshal(value)

    def test_schema_custom_format_invalid(self):

        class CustomFormatter(Formatter):
            def unmarshal(self, value):
                raise ValueError
        formatter = CustomFormatter()
        custom_format = 'custom'
        custom_formatters = {
            custom_format: formatter,
        }
        schema = Schema(
            'string',
            schema_format=custom_format,
            _source={'type': 'string', 'format': 'custom'},
        )
        media_type = MediaType('application/json', schema=schema)
        value = 'test'

        with pytest.raises(InvalidMediaTypeValue):
            media_type.unmarshal(
                value, custom_formatters=custom_formatters)
