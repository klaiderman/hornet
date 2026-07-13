from dataclasses import dataclass

from hornet.entities import CarStatus

@dataclass(slots=True)
class AddCar:
    model: str
    year: int
    status: CarStatus
