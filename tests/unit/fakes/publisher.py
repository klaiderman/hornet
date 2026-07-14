from hornet.events import RentalEvent

class FakePublisher:
    def __init__(self) -> None:
        self.events: list[RentalEvent] = []

    def publish(self, event: RentalEvent) -> None:
        self.events.append(event)
