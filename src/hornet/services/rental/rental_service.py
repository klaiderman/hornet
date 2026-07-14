import logging
from datetime import date

from hornet.commands import EndRental, RegisterRental
from hornet.entities import Car, CarStatus, Rental, can_transition
from hornet.events import RentalEvent
from hornet.exceptions import (
    CarNotFound,
    CarUnavailable,
    IllegalStatusTransition,
    RentalAlreadyEnded,
    RentalNotFound,
)
from hornet.ports import CarRepository, RentalEventPublisher, RentalRepository, RentalService

logger = logging.getLogger(__name__)

class RentalServiceImpl(RentalService):
    def __init__(self, cars: CarRepository, rentals: RentalRepository, publisher: RentalEventPublisher) -> None:
        self.cars = cars
        self.rentals = rentals
        self.publisher = publisher

    def register_rental(self, command: RegisterRental) -> Rental:
        car = self.cars.get(command.car_id)

        if car is None:
            raise CarNotFound(command.car_id)

        if not car.is_available:
            raise CarUnavailable(command.car_id)

        rental = self.rentals.add(
            Rental(
                id=None,
                car_id=command.car_id,
                customer_name=command.customer_name,
                start_date=command.start_date,
                end_date=None,
            )
        )

        self._move_car(car, CarStatus.in_use)
        self.publisher.publish(RentalEvent.of("rental.started", rental))
        logger.info("rental registered", extra={"action": "register", "entity": "rental", "entity_id": str(rental.id)})

        return rental

    def end_rental(self, command: EndRental) -> Rental:
        rental = self.rentals.get(command.rental_id)

        if rental is None:
            raise RentalNotFound(command.rental_id)

        if not rental.is_open:
            raise RentalAlreadyEnded(command.rental_id)

        rental.end_date = command.end_date or date.today()
        rental = self.rentals.end(rental)
        car = self.cars.get(rental.car_id)

        if car is None:
            raise CarNotFound(rental.car_id)

        self._move_car(car, CarStatus.available)
        self.publisher.publish(RentalEvent.of("rental.ended", rental))
        logger.info("rental ended", extra={"action": "end", "entity": "rental", "entity_id": str(rental.id)})

        return rental

    def list_rentals(self, open_only: bool, limit: int | None, offset: int) -> list[Rental]:
        if open_only:
            return self.rentals.find_open(limit, offset)

        return self.rentals.find_all(limit, offset)

    def _move_car(self, car: Car, target: CarStatus) -> None:
        if not can_transition(car.status, target):
            raise IllegalStatusTransition(car.status, target)

        car.status = target
        self.cars.update(car)
