from polyfactory.factories.pydantic_factory import ModelFactory

from hornet.entities import CarStatus
from hornet.schemas import CarCreate

class CarCreateFactory(ModelFactory[CarCreate]):
    status = CarStatus.available
