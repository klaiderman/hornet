import uvicorn
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from hornet.core import get_settings, instrument
from hornet.routers import car_router, health_router, install_error_handlers, rental_router
from hornet.runner import lifespan

class Application:
    def __init__(self) -> None:
        self._app = FastAPI(title="hornet", lifespan=lifespan)
        self._server: uvicorn.Server | None = None
        self._configure_rate_limiting()
        self._register_error_handlers()
        self._register_metrics()
        self._include_car_routes()
        self._include_rental_routes()
        self._include_health_routes()

    @property
    def app(self) -> FastAPI:
        return self._app

    def run(self) -> None:
        settings = get_settings()
        self._server = uvicorn.Server(uvicorn.Config(self._app, host=settings.host, port=settings.port))
        self._server.run()

    def stop(self) -> None:
        if self._server is None:
            return
        self._server.should_exit = True

    def reboot(self) -> None:
        self.stop()
        self.run()

    def _configure_rate_limiting(self) -> None:
        limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
        self._app.state.limiter = limiter
        self._app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        self._app.add_middleware(SlowAPIMiddleware)

    def _register_error_handlers(self) -> None:
        install_error_handlers(self._app)

    def _register_metrics(self) -> None:
        instrument(self._app)

    def _include_car_routes(self) -> None:
        self._app.include_router(car_router)

    def _include_rental_routes(self) -> None:
        self._app.include_router(rental_router)

    def _include_health_routes(self) -> None:
        self._app.include_router(health_router)

application = Application()
app = application.app

if __name__ == "__main__":
    application.run()
