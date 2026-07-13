from http import HTTPStatus

from hornet.decorators import http_status
from hornet.entities import CarStatus
from hornet.exceptions.base import DomainError

@http_status(HTTPStatus.CONFLICT)
class IllegalStatusTransition(DomainError):
    def __init__(self, current: CarStatus, target: CarStatus) -> None:
        super().__init__(f"illegal transition {current} -> {target}")
        self.current = current
        self.target = target
