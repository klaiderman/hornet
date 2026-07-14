from typing import Protocol

from hornet.events import RentalEvent

class RentalEventPublisher(Protocol):
    def publish(self, event: RentalEvent) -> None: ...
