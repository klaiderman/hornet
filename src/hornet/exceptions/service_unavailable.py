from http import HTTPStatus

from hornet.decorators import http_status
from hornet.exceptions.base import DomainError

@http_status(HTTPStatus.SERVICE_UNAVAILABLE)
class ServiceUnavailable(DomainError):
    def __init__(self) -> None:
        super().__init__("service unavailable")
