from polyfactory.factories.dataclass_factory import DataclassFactory

from hornet.commands import AddCar
from hornet.entities import CarStatus

class AddCarFactory(DataclassFactory[AddCar]):
    status = CarStatus.available
