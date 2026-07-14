from polyfactory.factories.dataclass_factory import DataclassFactory

from hornet.commands import AddCar
from hornet.core.config import get_settings
from hornet.core.database import make_engine, make_session_factory
from hornet.entities import Car
from hornet.repositories import SqlCarRepository

class AddCarFactory(DataclassFactory[AddCar]):
    pass

def seed(count: int = 5) -> None:
    settings = get_settings()
    session = make_session_factory(make_engine(settings.database_url))()
    try:
        repo = SqlCarRepository(session)
        for command in AddCarFactory.batch(count):
            car = repo.add(Car(id=None, model=command.model, year=command.year, status=command.status))
            print(f"created car id={car.id} model={car.model} year={car.year} status={car.status}")
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    seed()
