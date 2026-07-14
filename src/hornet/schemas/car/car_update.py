from pydantic import BaseModel, ConfigDict, Field

from hornet.constants import MAX_NAME_LENGTH, MAX_YEAR, MIN_YEAR
from hornet.entities import CarStatus

class CarUpdate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model: str | None = Field(default=None, min_length=1, max_length=MAX_NAME_LENGTH)
    year: int | None = Field(default=None, ge=MIN_YEAR, le=MAX_YEAR)
    status: CarStatus | None = None
