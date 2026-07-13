from http import HTTPStatus

from hornet.decorators import http_status
from hornet.exceptions.base import DomainError

@http_status(HTTPStatus.CONFLICT)
class CarHasRentals(DomainError):
    def __init__(self, car_id: int) -> None:
        super().__init__(f"car {car_id} has rentals")
        self.car_id = car_id
