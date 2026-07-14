from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query

from hornet.commands import EndRental, RegisterRental
from hornet.dependencies import RentalServiceDep, ResourceId
from hornet.schemas import ApiResponse, RentalCreate, RentalFilter, RentalRead

router = APIRouter(prefix="/rentals", tags=["rentals"])

@router.post("", response_model=ApiResponse[RentalRead], status_code=HTTPStatus.CREATED)
def create_rental(payload: RentalCreate, service: RentalServiceDep) -> ApiResponse[RentalRead]:
    command = RegisterRental(car_id=payload.car_id, customer_name=payload.customer_name, start_date=payload.start_date)
    rental = service.register_rental(command)

    return ApiResponse.ok(RentalRead.model_validate(rental))

@router.post("/{rental_id}/end", response_model=ApiResponse[RentalRead])
def end_rental(rental_id: ResourceId, service: RentalServiceDep) -> ApiResponse[RentalRead]:
    rental = service.end_rental(EndRental(rental_id))

    return ApiResponse.ok(RentalRead.model_validate(rental))

@router.get("", response_model=ApiResponse[list[RentalRead]])
def list_rentals(filters: Annotated[RentalFilter, Query()], service: RentalServiceDep) -> ApiResponse[list[RentalRead]]:
    rentals = service.list_rentals(filters.open_only, filters.limit, filters.offset)

    return ApiResponse.ok([RentalRead.model_validate(rental) for rental in rentals])
