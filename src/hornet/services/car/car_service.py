import logging

from hornet.commands import AddCar, UpdateCar
from hornet.entities import Car, CarStatus, can_transition
from hornet.exceptions import CarHasRentals, CarNotFound, IllegalStatusTransition
from hornet.ports import CarRepository, CarService, RentalRepository

logger = logging.getLogger(__name__)

class CarServiceImpl(CarService):
    def __init__(self, cars: CarRepository, rentals: RentalRepository) -> None:
        self.cars = cars
        self.rentals = rentals

    def add_car(self, command: AddCar) -> Car:
        car = self.cars.add(Car(id=None, model=command.model, year=command.year, status=command.status))
        logger.info("car added", extra={"action": "add", "entity": "car", "entity_id": str(car.id)})

        return car

    def update_car(self, command: UpdateCar) -> Car:
        car = self.cars.get(command.car_id)

        if car is None:
            raise CarNotFound(command.car_id)

        if command.status is not None and command.status != car.status:
            if command.status is CarStatus.in_use:
                raise IllegalStatusTransition(car.status, command.status)

            if self.rentals.get_open_for_car(command.car_id) is not None:
                raise IllegalStatusTransition(car.status, command.status)

            if not can_transition(car.status, command.status):
                raise IllegalStatusTransition(car.status, command.status)

            car.status = command.status

        if command.model is not None:
            car.model = command.model
        if command.year is not None:
            car.year = command.year

        car = self.cars.update(car)
        logger.info("car updated", extra={"action": "update", "entity": "car", "entity_id": str(command.car_id)})

        return car

    def delete_car(self, car_id: int) -> None:
        if self.rentals.has_any_for_car(car_id):
            raise CarHasRentals(car_id)

        if self.cars.get(car_id) is None:
            raise CarNotFound(car_id)

        self.cars.delete(car_id)
        logger.info("car deleted", extra={"action": "delete", "entity": "car", "entity_id": str(car_id)})

    def list_cars(self, status: CarStatus | None, limit: int | None, offset: int) -> list[Car]:
        return self.cars.find_all(status=status, limit=limit, offset=offset)
