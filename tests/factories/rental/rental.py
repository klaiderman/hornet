from polyfactory.factories.dataclass_factory import DataclassFactory

from hornet.entities import Rental

class RentalFactory(DataclassFactory[Rental]):
    end_date = None
