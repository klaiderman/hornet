from dataclasses import dataclass

from hornet.entities import CarStatus

@dataclass(slots=True)
class UpdateCar:
    car_id: int
    model: str | None
    year: int | None
    status: CarStatus | None
