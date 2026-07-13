from datetime import date

from pydantic import BaseModel, ConfigDict

class RentalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    car_id: int
    customer_name: str
    start_date: date
    end_date: date | None
