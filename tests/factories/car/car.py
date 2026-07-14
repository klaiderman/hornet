from polyfactory.factories.dataclass_factory import DataclassFactory

from hornet.entities import Car, CarStatus

class CarFactory(DataclassFactory[Car]):
    status = CarStatus.available
