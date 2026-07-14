from hornet.entities import Rental

class FakeRentalRepository:
    def __init__(self) -> None:
        self._rows: dict[int, Rental] = {}
        self._next_id = 1

    def add(self, rental: Rental) -> Rental:
        rental_id = self._next_id
        self._next_id += 1
        stored = Rental(
            id=rental_id,
            car_id=rental.car_id,
            customer_name=rental.customer_name,
            start_date=rental.start_date,
            end_date=rental.end_date,
        )
        self._rows[rental_id] = stored
        return stored

    def get(self, rental_id: int) -> Rental | None:
        return self._rows.get(rental_id)

    def get_open_for_car(self, car_id: int) -> Rental | None:
        for rental in self._rows.values():
            if rental.car_id == car_id and rental.end_date is None:
                return rental
        return None

    def find_all(self, limit: int | None = None, offset: int = 0) -> list[Rental]:
        rows = list(self._rows.values())[offset:]
        return rows if limit is None else rows[:limit]

    def find_open(self, limit: int | None = None, offset: int = 0) -> list[Rental]:
        rows = [r for r in self._rows.values() if r.end_date is None][offset:]
        return rows if limit is None else rows[:limit]

    def end(self, rental: Rental) -> Rental:
        self._rows[rental.id] = rental
        return rental

    def count_open(self) -> int:
        return len([r for r in self._rows.values() if r.end_date is None])

    def has_any_for_car(self, car_id: int) -> bool:
        return any(r.car_id == car_id for r in self._rows.values())
