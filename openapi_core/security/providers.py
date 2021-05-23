from typing import Dict, Optional
import warnings

from openapi_core.security.exceptions import SecurityError
from openapi_core.validation.request.datatypes import OpenAPIRequest


class BaseProvider:

    def __init__(self, scheme):
        self.scheme = scheme

    def __call__(self, request: OpenAPIRequest) -> Optional[str]:
        raise NotImplementedError


class UnsupportedProvider(BaseProvider):

    def __call__(self, request: OpenAPIRequest) -> None:
        warnings.warn("Unsupported scheme type")


class ApiKeyProvider(BaseProvider):

    def __call__(self, request: OpenAPIRequest) -> str:
        name = self.scheme['name']
        location = self.scheme['in']
        source: Dict[str, str] = getattr(request.parameters, location)
        if name not in source:
            raise SecurityError("Missing api key parameter.")
        return source[name]


class HttpProvider(BaseProvider):

    def __call__(self, request: OpenAPIRequest) -> str:
        if 'Authorization' not in request.parameters.header:
            raise SecurityError('Missing authorization header.')
        auth_header: str = request.parameters.header['Authorization']
        try:
            auth_type, encoded_credentials = auth_header.split(' ', 1)
        except ValueError:
            raise SecurityError('Could not parse authorization header.')

        scheme = self.scheme['scheme']
        if auth_type.lower() != scheme:
            raise SecurityError(
                f'Unknown authorization method {auth_type}')

        return encoded_credentials
