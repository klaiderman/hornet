from pydantic import BaseModel, Field

from hornet.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from hornet.entities import CarStatus

class CarFilter(BaseModel):
    status: CarStatus | None = None
    limit: int = Field(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE)
    offset: int = Field(default=0, ge=0)
