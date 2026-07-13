from pydantic import BaseModel, Field

class RentalFilter(BaseModel):
    open_only: bool = False
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
