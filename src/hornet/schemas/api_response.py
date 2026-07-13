from typing import Self

from pydantic import BaseModel

from hornet.schemas.api_error import ApiError

class ApiResponse[T](BaseModel):
    is_success: bool
    data: T | None = None
    error: ApiError | None = None

    @classmethod
    def ok(cls, data: T) -> Self:
        return cls(is_success=True, data=data)

    @classmethod
    def failure(cls, error: ApiError) -> Self:
        return cls(is_success=False, error=error)
