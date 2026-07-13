from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from hornet.entities import Rental

@dataclass(frozen=True, slots=True)
class RentalEvent:
    type: str
    rental_id: int
    car_id: int
    customer_name: str
    start_date: date
    end_date: date | None

    @classmethod
    def of(cls, event_type: str, rental: Rental) -> RentalEvent:
        return cls(
            type=event_type,
            rental_id=rental.id,
            car_id=rental.car_id,
            customer_name=rental.customer_name,
            start_date=rental.start_date,
            end_date=rental.end_date,
        )
