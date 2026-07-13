from datetime import date

from pydantic import BaseModel, Field

class RentalCreate(BaseModel):
    car_id: int
    customer_name: str = Field(min_length=1, max_length=100)
    start_date: date
