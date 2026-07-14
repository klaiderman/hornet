import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from hornet.core.config import get_settings
from hornet.main import Application

@pytest.fixture(scope="session")
def database_url():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        url = postgres.get_connection_url()
        config = Config("alembic.ini")
        config.set_main_option("sqlalchemy.url", url)
        command.upgrade(config, "head")
        yield url

@pytest.fixture
def session_factory(database_url):
    engine = create_engine(database_url)
    yield sessionmaker(bind=engine, expire_on_commit=False)
    engine.dispose()

@pytest.fixture
def client(database_url, monkeypatch):
    monkeypatch.setenv("HORNET_DATABASE_URL", database_url)
    monkeypatch.setenv("HORNET_REDIS_URL", "redis://localhost:6390/0")
    get_settings.cache_clear()
    with TestClient(Application().app) as test_client:
        yield test_client
    get_settings.cache_clear()
