"""OpenAPI core contrib falcon handlers module"""
from json import dumps
from typing import List

from falcon import Request, Response, status_codes
from falcon.constants import MEDIA_JSON

from openapi_core.exceptions import MissingRequiredParameter, OpenAPIError
from openapi_core.templating.media_types.exceptions import MediaTypeNotFound
from openapi_core.templating.paths.exceptions import (
    ServerNotFound, OperationNotFound, PathNotFound,
)
from openapi_core.validation.exceptions import InvalidSecurity


class FalconOpenAPIErrorsHandler:

    OPENAPI_ERROR_STATUS = {
        MissingRequiredParameter: 400,
        ServerNotFound: 400,
        InvalidSecurity: 403,
        OperationNotFound: 405,
        PathNotFound: 404,
        MediaTypeNotFound: 415,
    }

    @classmethod
    def handle(cls, req: Request, resp: Response, errors: List[OpenAPIError]):
        data_errors = [
            cls.format_openapi_error(err)
            for err in errors
        ]
        data = {
            'errors': data_errors,
        }
        data_str = dumps(data)
        data_error_max = max(data_errors, key=cls.get_error_status)
        resp.content_type = MEDIA_JSON
        resp.status = getattr(
            status_codes, f"HTTP_{data_error_max['status']}",
            status_codes.HTTP_400,
        )
        resp.text = data_str
        resp.complete = True

    @classmethod
    def format_openapi_error(cls, error: OpenAPIError) -> dict:
        return {
            'title': str(error),
            'status': cls.OPENAPI_ERROR_STATUS.get(error.__class__, 400),
            'class': str(type(error)),
        }

    @classmethod
    def get_error_status(cls, error: dict) -> str:
        return error['status']
