from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hornet.entities import Rental
from hornet.exceptions import CarUnavailable, RentalNotFound
from hornet.models import RentalModel
from hornet.ports import RentalRepository

class SqlRentalRepository(RentalRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _to_rental(row: RentalModel) -> Rental:
        return Rental(
            id=row.id,
            car_id=row.car_id,
            customer_name=row.customer_name,
            start_date=row.start_date,
            end_date=row.end_date,
        )

    def add(self, rental: Rental) -> Rental:
        row = RentalModel(
            car_id=rental.car_id,
            customer_name=rental.customer_name,
            start_date=rental.start_date,
            end_date=rental.end_date,
        )

        self.session.add(row)

        try:
            self.session.flush()
        except IntegrityError:
            raise CarUnavailable(rental.car_id) from None

        return self._to_rental(row)

    def get(self, rental_id: int) -> Rental | None:
        row = self.session.get(RentalModel, rental_id)

        if row is None:
            return None

        return self._to_rental(row)

    def get_open_for_car(self, car_id: int) -> Rental | None:
        stmt = select(RentalModel).where(RentalModel.car_id == car_id, RentalModel.end_date.is_(None))

        row = self.session.execute(stmt).scalars().first()

        if row is None:
            return None

        return self._to_rental(row)

    def find_all(self, limit: int | None = None, offset: int = 0) -> list[Rental]:
        stmt = select(RentalModel).order_by(RentalModel.id).offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        return [self._to_rental(row) for row in self.session.execute(stmt).scalars()]

    def find_open(self, limit: int | None = None, offset: int = 0) -> list[Rental]:
        stmt = select(RentalModel).where(RentalModel.end_date.is_(None)).order_by(RentalModel.id).offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        return [self._to_rental(row) for row in self.session.execute(stmt).scalars()]

    def end(self, rental: Rental) -> Rental:
        row = self.session.get(RentalModel, rental.id)

        if row is None:
            raise RentalNotFound(rental.id)

        row.end_date = rental.end_date
        self.session.flush()

        return self._to_rental(row)

    def count_open(self) -> int:
        stmt = select(func.count()).select_from(RentalModel).where(RentalModel.end_date.is_(None))
        return self.session.execute(stmt).scalar_one()

    def has_any_for_car(self, car_id: int) -> bool:
        stmt = select(func.count()).select_from(RentalModel).where(RentalModel.car_id == car_id)
        return self.session.execute(stmt).scalar_one() > 0
