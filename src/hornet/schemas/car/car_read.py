from pydantic import BaseModel, ConfigDict

from hornet.entities import CarStatus

class CarRead(BaseModel):
    model_config = ConfigDict(protected_namespaces=(), from_attributes=True)

    id: int
    model: str
    year: int
    status: CarStatus
