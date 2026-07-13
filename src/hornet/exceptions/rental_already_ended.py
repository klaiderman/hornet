from http import HTTPStatus

from hornet.decorators import http_status
from hornet.exceptions.base import DomainError

@http_status(HTTPStatus.CONFLICT)
class RentalAlreadyEnded(DomainError):
    def __init__(self, rental_id: int) -> None:
        super().__init__(f"rental {rental_id} already ended")
        self.rental_id = rental_id
