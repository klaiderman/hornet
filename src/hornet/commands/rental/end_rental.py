from dataclasses import dataclass
from datetime import date

@dataclass(slots=True)
class EndRental:
    rental_id: int
    end_date: date | None = None
