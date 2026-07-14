from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from hornet.dependencies.session import get_session
from hornet.ports import CarService
from hornet.repositories import SqlCarRepository, SqlRentalRepository
from hornet.services import CarServiceImpl

def get_car_service(session: Session = Depends(get_session)) -> CarService:
    return CarServiceImpl(SqlCarRepository(session), SqlRentalRepository(session))

CarServiceDep = Annotated[CarService, Depends(get_car_service)]
