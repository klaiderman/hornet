from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from hornet.dependencies.session import get_session
from hornet.ports import RentalService
from hornet.repositories import SqlCarRepository, SqlRentalRepository
from hornet.services import RentalServiceImpl

def get_rental_service(request: Request, session: Session = Depends(get_session)) -> RentalService:
    return RentalServiceImpl(SqlCarRepository(session), SqlRentalRepository(session), request.app.state.publisher)

RentalServiceDep = Annotated[RentalService, Depends(get_rental_service)]
