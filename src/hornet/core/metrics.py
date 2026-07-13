import contextlib
import time
from collections.abc import Callable

from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator

def cached(fn: Callable[[], int], ttl_seconds: float = 5.0) -> Callable[[], int]:
    state: dict[str, object] = {"value": None, "ts": None}

    def run() -> int:
        now = time.monotonic()
        if state["ts"] is not None and now - state["ts"] < ttl_seconds:
            return state["value"]
        value = fn()
        state["value"] = value
        state["ts"] = now
        return value
    return run

def register_business_metrics(active_cars: Callable[[], int], ongoing_rentals: Callable[[], int]) -> None:
    with contextlib.suppress(ValueError):
        Gauge("hornet_active_cars", "Number of active cars").set_function(active_cars)
    with contextlib.suppress(ValueError):
        Gauge("hornet_ongoing_rentals", "Number of ongoing rentals").set_function(ongoing_rentals)

def instrument(app) -> None:
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
