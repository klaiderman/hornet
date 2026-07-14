from hornet.entities import Car, CarStatus

class FakeCarRepository:
    def __init__(self) -> None:
        self._rows: dict[int, Car] = {}
        self._next_id = 1

    def add(self, car: Car) -> Car:
        car_id = self._next_id
        self._next_id += 1
        stored = Car(id=car_id, model=car.model, year=car.year, status=car.status)
        self._rows[car_id] = stored
        return stored

    def get(self, car_id: int) -> Car | None:
        return self._rows.get(car_id)

    def update(self, car: Car) -> Car:
        self._rows[car.id] = car
        return car

    def delete(self, car_id: int) -> None:
        self._rows.pop(car_id, None)

    def find_all(self, status: CarStatus | None = None, limit: int | None = None, offset: int = 0) -> list[Car]:
        rows = list(self._rows.values())
        if status is not None:
            rows = [c for c in rows if c.status == status]
        rows = rows[offset:]
        if limit is not None:
            rows = rows[:limit]
        return rows

    def count_by_status(self, status: CarStatus) -> int:
        return len([c for c in self._rows.values() if c.status == status])
