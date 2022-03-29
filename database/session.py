from typing import Optional

import databases
import sqlalchemy
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
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

engine = create_async_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)  # type: ignore
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=True)


database = databases.Database(SQLALCHEMY_DATABASE_URI)

metadata = sqlalchemy.MetaData()


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
       yield session
