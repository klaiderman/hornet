from pydantic import BaseModel, ConfigDict, Field

class CarCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1900, le=2100)
