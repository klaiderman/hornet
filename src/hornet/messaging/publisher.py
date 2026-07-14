import logging
from dataclasses import asdict

import redis
from prometheus_client import Counter

from hornet.events import RentalEvent
from hornet.ports import RentalEventPublisher

logger = logging.getLogger(__name__)
publish_failures = Counter("hornet_event_publish_failures_total", "Number of failed rental event publishes")

class RedisStreamPublisher(RentalEventPublisher):
    def __init__(self, client: redis.Redis, stream: str) -> None:
        self.client = client
        self.stream = stream

    def publish(self, event: RentalEvent) -> None:
        flat = {key: self._flatten(value) for key, value in asdict(event).items()}
        try:
            self.client.xadd(self.stream, flat)
        except redis.RedisError:
            publish_failures.inc()
            logger.warning("failed to publish %s to redis stream %s", event.type, self.stream)

    @staticmethod
    def _flatten(value: object) -> str:
        if value is None:
            return ""
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return str(value)
