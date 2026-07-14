from fastapi import APIRouter, Request

from hornet.core.database import ping
from hornet.exceptions import ServiceUnavailable
from hornet.schemas import ApiResponse

router = APIRouter()

@router.get("/healthz", response_model=ApiResponse[bool])
def healthz(request: Request) -> ApiResponse[bool]:
    try:
        ping(request.app.state.session_factory)
    except Exception:
        raise ServiceUnavailable() from None

    return ApiResponse.ok(True)
