from pydantic import BaseModel

class ApiError(BaseModel):
    type: str
    title: str
    status: int
    detail: str
