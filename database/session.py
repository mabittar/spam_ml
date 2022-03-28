from typing import Generator, Optional

import databases
import sqlalchemy
from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_DB, config

SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        user=POSTGRES_USER,
        password=str(POSTGRES_PASSWORD),
        port=POSTGRES_PORT,
        host=POSTGRES_SERVER,
        path=f"/{POSTGRES_DB or ''}",
    )

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)  # type: ignore
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


database = databases.Database(SQLALCHEMY_DATABASE_URI)

metadata = sqlalchemy.MetaData()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
