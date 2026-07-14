import contextlib
import logging
from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI

from hornet.core import (
    cached,
    get_settings,
    make_engine,
    make_session_factory,
    register_business_metrics,
    setup_logging,
)
from hornet.entities import CarStatus
from hornet.messaging import RedisStreamPublisher
from hornet.repositories import SqlCarRepository, SqlRentalRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.settings = settings
    engine = make_engine(settings.database_url)
    app.state.engine = engine
    app.state.session_factory = make_session_factory(engine)
    redis_client = redis.from_url(settings.redis_url)
    app.state.publisher = RedisStreamPublisher(redis_client, settings.rental_stream)

    setup_logging(settings.log_level, settings.log_file)

    def counting(query):
        def run() -> int:
            try:
                session = app.state.session_factory()
                try:
                    return query(session)
                finally:
                    session.close()
            except Exception:
                return 0
        return run

    register_business_metrics(
        active_cars=cached(
            counting(
                lambda s: sum(
                    SqlCarRepository(s).count_by_status(status)
                    for status in (CarStatus.available, CarStatus.in_use)
                )
            )
        ),
        ongoing_rentals=cached(counting(lambda s: SqlRentalRepository(s).count_open())),
    )

    yield

    for handler in list(logging.getLogger().handlers):
        with contextlib.suppress(Exception):
            handler.close()
    with contextlib.suppress(Exception):
        engine.dispose()
    with contextlib.suppress(Exception):
        redis_client.close()
