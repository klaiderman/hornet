from dataclasses import dataclass
from datetime import date

@dataclass(slots=True)
class RegisterRental:
    car_id: int
    customer_name: str
    start_date: date
