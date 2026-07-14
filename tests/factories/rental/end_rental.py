from polyfactory.factories.dataclass_factory import DataclassFactory

from hornet.commands import EndRental

class EndRentalFactory(DataclassFactory[EndRental]):
    end_date = None
