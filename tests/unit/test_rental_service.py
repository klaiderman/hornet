from datetime import date

import pytest

from hornet.entities import CarStatus
from hornet.exceptions import CarUnavailable, RentalAlreadyEnded, RentalNotFound
from tests.factories import CarFactory, EndRentalFactory, RegisterRentalFactory, RentalFactory

def test_register_rental_on_unavailable_car_raises(rental_service, car_repo):
    car = car_repo.add(CarFactory.build(status=CarStatus.under_maintenance))

    with pytest.raises(CarUnavailable):
        rental_service.register_rental(RegisterRentalFactory.build(car_id=car.id))

def test_end_rental_already_ended_raises(rental_service, car_repo, rental_repo):
    car = car_repo.add(CarFactory.build(status=CarStatus.in_use))
    rental = rental_repo.add(RentalFactory.build(car_id=car.id, end_date=date(2026, 1, 5)))

    with pytest.raises(RentalAlreadyEnded):
        rental_service.end_rental(EndRentalFactory.build(rental_id=rental.id))

def test_end_rental_not_found_raises(rental_service):
    with pytest.raises(RentalNotFound):
        rental_service.end_rental(EndRentalFactory.build(rental_id=999))

def test_happy_path_register_and_end_rental(rental_service, car_repo, rental_repo, publisher):
    car = car_repo.add(CarFactory.build(status=CarStatus.available))

    rental = rental_service.register_rental(RegisterRentalFactory.build(car_id=car.id))

    assert car_repo.get(car.id).status == CarStatus.in_use
    assert rental.is_open
    assert publisher.events[-1].type == "rental.started"

    ended = rental_service.end_rental(EndRentalFactory.build(rental_id=rental.id))

    assert not ended.is_open
    assert car_repo.get(car.id).status == CarStatus.available
    assert publisher.events[-1].type == "rental.ended"

def test_list_rentals_open_only(rental_service, rental_repo):
    rental_repo.add(RentalFactory.build(car_id=1))
    rental_repo.add(RentalFactory.build(car_id=2, end_date=date(2026, 1, 2)))

    result = rental_service.list_rentals(True, None, 0)

    assert len(result) == 1
    assert result[0].car_id == 1
