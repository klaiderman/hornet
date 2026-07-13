from pydantic import BaseModel, ConfigDict, Field

from hornet.entities import CarStatus

class CarUpdate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=1900, le=2100)
    status: CarStatus | None = None
