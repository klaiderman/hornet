from pydantic import BaseModel, Field

from hornet.entities import CarStatus

class CarFilter(BaseModel):
    status: CarStatus | None = None
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
