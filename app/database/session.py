from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.settings import SQLALCHEMY_DATABASE_URI

"""
Asyncpg has an issue when using PostgreSQL ENUM datatypes. 
To mitigate this issue, the PostgreSQL “jit” setting may be disabled
"""

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    connect_args={"server_settings": {"jit": "off"}}
)  # type: ignore

session_local = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=True)
ScopedSession = scoped_session(session_local)


async def get_session() -> AsyncGenerator:
    async with ScopedSession() as session:
        yield session
