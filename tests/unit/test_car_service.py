import pytest

from hornet.entities import CarStatus
from hornet.exceptions import CarHasRentals, CarNotFound, IllegalStatusTransition
from tests.factories import AddCarFactory, CarFactory, RentalFactory, UpdateCarFactory

def test_add_car(car_service, car_repo):
    command = AddCarFactory.build()

    car = car_service.add_car(command)

    assert car.id is not None
    assert car_repo.get(car.id).model == command.model

def test_delete_car_with_open_rental_raises(car_service, car_repo, rental_repo):
    car = car_repo.add(CarFactory.build(status=CarStatus.in_use))
    rental_repo.add(RentalFactory.build(car_id=car.id))

    with pytest.raises(CarHasRentals):
        car_service.delete_car(car.id)

def test_delete_car_without_open_rental_succeeds(car_service, car_repo):
    car = car_repo.add(CarFactory.build())

    car_service.delete_car(car.id)

    assert car_repo.get(car.id) is None

def test_delete_car_not_found_raises(car_service):
    with pytest.raises(CarNotFound):
        car_service.delete_car(999)

def test_update_car_illegal_transition_raises(car_service, car_repo):
    car = car_repo.add(CarFactory.build(status=CarStatus.under_maintenance))

    with pytest.raises(IllegalStatusTransition):
        car_service.update_car(UpdateCarFactory.build(car_id=car.id, status=CarStatus.in_use))

def test_update_car_legal_transition_applies(car_service, car_repo):
    car = car_repo.add(CarFactory.build(status=CarStatus.under_maintenance))

    updated = car_service.update_car(UpdateCarFactory.build(car_id=car.id, status=CarStatus.available))

    assert updated.status == CarStatus.available

def test_list_cars_filters_by_status(car_service, car_repo):
    car_repo.add(CarFactory.build(model="A", status=CarStatus.available))
    car_repo.add(CarFactory.build(model="B", status=CarStatus.in_use))

    result = car_service.list_cars(CarStatus.available, None, 0)

    assert [c.model for c in result] == ["A"]
