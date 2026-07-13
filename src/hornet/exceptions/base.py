from http import HTTPStatus

class DomainError(Exception):
    status = HTTPStatus.BAD_REQUEST
