from pydantic import BaseModel, ConfigDict, Field

from hornet.constants import MAX_NAME_LENGTH, MAX_YEAR, MIN_YEAR

class CarCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model: str = Field(min_length=1, max_length=MAX_NAME_LENGTH)
    year: int = Field(ge=MIN_YEAR, le=MAX_YEAR)
