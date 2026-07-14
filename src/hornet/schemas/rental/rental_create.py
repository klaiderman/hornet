from datetime import date

from pydantic import BaseModel, Field

from hornet.constants import MAX_NAME_LENGTH

class RentalCreate(BaseModel):
    car_id: int
    customer_name: str = Field(min_length=1, max_length=MAX_NAME_LENGTH)
    start_date: date
