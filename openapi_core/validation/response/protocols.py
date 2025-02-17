"""OpenAPI core validation response protocols module"""
from typing import TYPE_CHECKING
from typing import Optional

if TYPE_CHECKING:
    from typing_extensions import Protocol
    from typing_extensions import runtime_checkable
else:
    try:
        from typing import Protocol
        from typing import runtime_checkable
    except ImportError:
        from typing_extensions import Protocol
        from typing_extensions import runtime_checkable

from werkzeug.datastructures import Headers

from openapi_core.spec import Spec
from openapi_core.validation.request.protocols import Request
from openapi_core.validation.response.datatypes import ResponseValidationResult


@runtime_checkable
class Response(Protocol):
    """Response protocol.

    Attributes:
        data
            The response body, as string.
        status_code
            The status code as integer.
        headers
            Response headers as Headers.
        mimetype
            Lowercase content type without charset.
    """

    @property
    def data(self) -> str:
        ...

    @property
    def status_code(self) -> int:
        ...

    @property
    def mimetype(self) -> str:
        ...

    @property
    def headers(self) -> Headers:
        ...


@runtime_checkable
class ResponseValidator(Protocol):
    def validate(
        self,
        spec: Spec,
        request: Request,
        response: Response,
        base_url: Optional[str] = None,
    ) -> ResponseValidationResult:
        ...
