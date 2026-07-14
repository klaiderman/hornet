import pytest

from hornet.services import CarServiceImpl, RentalServiceImpl
from tests.unit.fakes import FakeCarRepository, FakePublisher, FakeRentalRepository

@pytest.fixture
def car_repo() -> FakeCarRepository:
    return FakeCarRepository()

@pytest.fixture
def rental_repo() -> FakeRentalRepository:
    return FakeRentalRepository()

@pytest.fixture
def publisher() -> FakePublisher:
    return FakePublisher()

@pytest.fixture
def car_service(car_repo, rental_repo) -> CarServiceImpl:
    return CarServiceImpl(car_repo, rental_repo)

@pytest.fixture
def rental_service(car_repo, rental_repo, publisher) -> RentalServiceImpl:
    return RentalServiceImpl(car_repo, rental_repo, publisher)
