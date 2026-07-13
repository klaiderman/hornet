from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

_PING = text("SELECT 1")

class Base(DeclarativeBase):
    pass

def make_engine(url: str) -> Engine:
    return create_engine(url, pool_pre_ping=True)

def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)

def ping(session_factory: sessionmaker[Session]) -> None:
    session = session_factory()
    try:
        session.execute(_PING)
    finally:
        session.close()
