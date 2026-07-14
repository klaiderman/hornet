from http import HTTPStatus

import pytest

from tests.factories import CarCreateFactory, RentalCreateFactory

pytestmark = pytest.mark.integration

def test_full_rental_lifecycle_over_http(client):
    created = client.post("/cars", json=CarCreateFactory.build().model_dump(mode="json"))

    assert created.status_code == HTTPStatus.CREATED

    car_id = created.json()["data"]["id"]

    rented = client.post("/rentals", json=RentalCreateFactory.build(car_id=car_id).model_dump(mode="json"))

    assert rented.status_code == HTTPStatus.CREATED

    rental_id = rented.json()["data"]["id"]

    in_use = client.get("/cars", params={"status": "in_use"}).json()["data"]

    assert any(car["id"] == car_id for car in in_use)

    conflict = client.post("/rentals", json=RentalCreateFactory.build(car_id=car_id).model_dump(mode="json"))

    assert conflict.status_code == HTTPStatus.CONFLICT
    assert conflict.json()["is_success"] is False
    assert conflict.json()["error"]["type"] == "CarUnavailable"

    ended = client.post(f"/rentals/{rental_id}/end")

    assert ended.status_code == HTTPStatus.OK
    assert ended.json()["data"]["end_date"] is not None

    available = client.get("/cars", params={"status": "available"}).json()["data"]

    assert any(car["id"] == car_id for car in available)

def test_healthz_and_metrics(client):
    health = client.get("/healthz")

    assert health.status_code == HTTPStatus.OK
    assert health.json() == {"is_success": True, "data": True, "error": None}

    body = client.get("/metrics").text

    assert "hornet_active_cars" in body
    assert "hornet_ongoing_rentals" in body
