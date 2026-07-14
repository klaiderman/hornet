from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query

from hornet.commands import AddCar, UpdateCar
from hornet.dependencies import CarServiceDep, ResourceId
from hornet.entities import CarStatus
from hornet.schemas import ApiResponse, CarCreate, CarFilter, CarRead, CarUpdate

router = APIRouter(prefix="/cars", tags=["cars"])

@router.post("", response_model=ApiResponse[CarRead], status_code=HTTPStatus.CREATED)
def create_car(payload: CarCreate, service: CarServiceDep) -> ApiResponse[CarRead]:
    car = service.add_car(AddCar(model=payload.model, year=payload.year, status=CarStatus.available))

    return ApiResponse.ok(CarRead.model_validate(car))

@router.get("", response_model=ApiResponse[list[CarRead]])
def list_cars(query: Annotated[CarFilter, Query()], service: CarServiceDep) -> ApiResponse[list[CarRead]]:
    cars = service.list_cars(query.status, query.limit, query.offset)

    return ApiResponse.ok([CarRead.model_validate(car) for car in cars])

@router.patch("/{car_id}", response_model=ApiResponse[CarRead])
def update_car(car_id: ResourceId, payload: CarUpdate, service: CarServiceDep) -> ApiResponse[CarRead]:
    command = UpdateCar(car_id=car_id, model=payload.model, year=payload.year, status=payload.status)
    car = service.update_car(command)

    return ApiResponse.ok(CarRead.model_validate(car))

@router.delete("/{car_id}", response_model=ApiResponse[bool])
def delete_car(car_id: ResourceId, service: CarServiceDep) -> ApiResponse[bool]:
    service.delete_car(car_id)

    return ApiResponse.ok(True)
