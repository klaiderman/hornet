from http import HTTPStatus

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from hornet.dependencies import get_car_service, get_rental_service
from hornet.routers import car_router, install_error_handlers
from hornet.services import CarServiceImpl, RentalServiceImpl
from tests.factories import CarCreateFactory, RentalFactory

@pytest.fixture
def app(car_repo, rental_repo, publisher) -> FastAPI:
    app = FastAPI()
    install_error_handlers(app)
    app.include_router(car_router)

    car_service = CarServiceImpl(car_repo, rental_repo)
    rental_service = RentalServiceImpl(car_repo, rental_repo, publisher)

    app.dependency_overrides[get_car_service] = lambda: car_service
    app.dependency_overrides[get_rental_service] = lambda: rental_service

    return app

@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)

def test_create_car_wraps_data_in_envelope(client):
    payload = CarCreateFactory.build()

    response = client.post("/cars", json=payload.model_dump(mode="json"))

    assert response.status_code == HTTPStatus.CREATED

    envelope = response.json()

    assert envelope["is_success"] is True
    assert envelope["error"] is None
    assert envelope["data"]["model"] == payload.model
    assert envelope["data"]["id"] is not None

def test_list_cars_returns_created_cars(client):
    first = CarCreateFactory.build()
    second = CarCreateFactory.build()
    client.post("/cars", json=first.model_dump(mode="json"))
    client.post("/cars", json=second.model_dump(mode="json"))

    response = client.get("/cars")

    assert response.status_code == HTTPStatus.OK

    models = {car["model"] for car in response.json()["data"]}

    assert {first.model, second.model} <= models

def test_delete_car_success_returns_envelope(client):
    created = client.post("/cars", json=CarCreateFactory.build().model_dump(mode="json"))
    car_id = created.json()["data"]["id"]

    response = client.delete(f"/cars/{car_id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"is_success": True, "data": True, "error": None}

def test_delete_car_with_open_rental_returns_409_envelope(client, car_repo, rental_repo):
    created = client.post("/cars", json=CarCreateFactory.build().model_dump(mode="json"))
    car_id = created.json()["data"]["id"]

    rental_repo.add(RentalFactory.build(car_id=car_id))

    response = client.delete(f"/cars/{car_id}")

    assert response.status_code == HTTPStatus.CONFLICT

    envelope = response.json()

    assert envelope["is_success"] is False
    assert envelope["error"]["type"] == "CarHasRentals"
    assert envelope["error"]["status"] == HTTPStatus.CONFLICT
