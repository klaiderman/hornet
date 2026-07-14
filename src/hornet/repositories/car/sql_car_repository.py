from sqlalchemy import func, select
from sqlalchemy.orm import Session

from hornet.entities import Car, CarStatus
from hornet.exceptions import CarNotFound
from hornet.models import CarModel
from hornet.ports import CarRepository

class SqlCarRepository(CarRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _to_car(row: CarModel) -> Car:
        return Car(id=row.id, model=row.model, year=row.year, status=row.status)

    def add(self, car: Car) -> Car:
        row = CarModel(model=car.model, year=car.year, status=car.status)

        self.session.add(row)
        self.session.flush()

        return self._to_car(row)

    def get(self, car_id: int) -> Car | None:
        row = self.session.get(CarModel, car_id)

        if row is None:
            return None

        return self._to_car(row)

    def update(self, car: Car) -> Car:
        row = self.session.get(CarModel, car.id)

        if row is None:
            raise CarNotFound(car.id)

        row.model, row.year, row.status = car.model, car.year, car.status
        self.session.flush()

        return self._to_car(row)

    def delete(self, car_id: int) -> None:
        row = self.session.get(CarModel, car_id)

        if row is None:
            raise CarNotFound(car_id)

        self.session.delete(row)
        self.session.flush()

    def find_all(self, status: CarStatus | None = None, limit: int | None = None, offset: int = 0) -> list[Car]:
        stmt = select(CarModel).order_by(CarModel.id).offset(offset)

        if status is not None:
            stmt = stmt.where(CarModel.status == status)

        if limit is not None:
            stmt = stmt.limit(limit)

        return [self._to_car(row) for row in self.session.execute(stmt).scalars()]

    def count_by_status(self, status: CarStatus) -> int:
        stmt = select(func.count()).select_from(CarModel).where(CarModel.status == status)
        return self.session.execute(stmt).scalar_one()
