from collections.abc import Callable
from http import HTTPStatus

def http_status(code: HTTPStatus) -> Callable[[type], type]:
    def apply(cls: type) -> type:
        cls.status = code
        return cls
    return apply
