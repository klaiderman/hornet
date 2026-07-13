from http import HTTPStatus

from hornet.decorators import http_status
from hornet.exceptions.base import DomainError

@http_status(HTTPStatus.NOT_FOUND)
class RentalNotFound(DomainError):
    def __init__(self, rental_id: int) -> None:
        super().__init__(f"rental {rental_id} not found")
        self.rental_id = rental_id
