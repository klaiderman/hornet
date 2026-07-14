from polyfactory.factories.dataclass_factory import DataclassFactory

from hornet.commands import UpdateCar

class UpdateCarFactory(DataclassFactory[UpdateCar]):
    model = None
    year = None
    status = None
