import pytest

from hornet.entities import CarStatus
from hornet.exceptions import CarUnavailable
from hornet.repositories import SqlCarRepository, SqlRentalRepository
from hornet.services import CarServiceImpl, RentalServiceImpl
from tests.factories import AddCarFactory, CarFactory, EndRentalFactory, RegisterRentalFactory, RentalFactory
from tests.unit.fakes import FakePublisher

pytestmark = pytest.mark.integration

def test_register_and_end_persists_status(session_factory):
    session = session_factory()

    try:
        cars = SqlCarRepository(session)
        rentals = SqlRentalRepository(session)

        car = CarServiceImpl(cars, rentals).add_car(AddCarFactory.build())
        rental = RentalServiceImpl(cars, rentals, FakePublisher()).register_rental(
            RegisterRentalFactory.build(car_id=car.id)
        )
        session.commit()

        assert cars.get(car.id).status is CarStatus.in_use

        RentalServiceImpl(cars, rentals, FakePublisher()).end_rental(EndRentalFactory.build(rental_id=rental.id))
        session.commit()

        assert cars.get(car.id).is_available
    finally:
        session.close()

def test_partial_unique_index_blocks_two_open_rentals(session_factory):
    session = session_factory()

    try:
        cars = SqlCarRepository(session)
        rentals = SqlRentalRepository(session)

        car = cars.add(CarFactory.build(status=CarStatus.available))
        rentals.add(RentalFactory.build(car_id=car.id))

        with pytest.raises(CarUnavailable):
            rentals.add(RentalFactory.build(car_id=car.id))
    finally:
        session.rollback()
        session.close()
