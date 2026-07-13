from dataclasses import dataclass
from datetime import date

@dataclass(slots=True)
class Rental:
    id: int | None
    car_id: int
    customer_name: str
    start_date: date
    end_date: date | None

    @property
    def is_open(self) -> bool:
        return self.end_date is None
