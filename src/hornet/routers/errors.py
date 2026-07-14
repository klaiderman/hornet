import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from hornet.exceptions import DomainError
from hornet.helpers import to_title
from hornet.schemas import ApiError, ApiResponse

logger = logging.getLogger(__name__)

def _error_response(error_type: str, title: str, status: HTTPStatus, detail: str) -> JSONResponse:
    body = ApiResponse.failure(ApiError(type=error_type, title=title, status=status, detail=detail))
    return JSONResponse(status_code=status, content=body.model_dump())

def install_error_handlers(app: FastAPI) -> None:
    async def handler(request: Request, exc: DomainError) -> JSONResponse:
        name = type(exc).__name__
        logger.warning(str(exc), extra={"action": "error", "entity": name, "entity_id": None})

        return _error_response(name, to_title(name), exc.status, str(exc))

    async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning(str(exc), extra={"action": "error", "entity": "ValidationError", "entity_id": None})

        return _error_response("ValidationError", "Validation Error", HTTPStatus.UNPROCESSABLE_ENTITY, str(exc))

    async def unhandled_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.warning(str(exc), extra={"action": "error", "entity": "InternalError", "entity_id": None})

        return _error_response("InternalError", "Internal Error", HTTPStatus.INTERNAL_SERVER_ERROR, "internal error")

    app.add_exception_handler(DomainError, handler)
    app.add_exception_handler(RequestValidationError, validation_handler)
    app.add_exception_handler(Exception, unhandled_handler)
