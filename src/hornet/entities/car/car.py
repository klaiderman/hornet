from dataclasses import dataclass

from hornet.entities.car.car_status import CarStatus

@dataclass(slots=True)
class Car:
    id: int | None
    model: str
    year: int
    status: CarStatus

    @property
    def is_available(self) -> bool:
        return self.status is CarStatus.available
