from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import get_settings


engine = create_engine(
    get_settings().database_url,
    connect_args={"check_same_thread": False},
    echo=True
)

Base = declarative_base()


def session_mk() -> Session:
    return sessionmaker(engine)()


def get_db():
    """Rely on FastAPI dependency injection"""
    session = sessionmaker(engine, autoflush=False)()
    try:
        yield session
    finally:
        session.close()


def init_db():
    Base.metadata.create_all(engine)
