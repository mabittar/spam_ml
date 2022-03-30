
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.settings import SQLALCHEMY_DATABASE_URI


engine = create_async_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)  # type: ignore
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=True)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
       yield session
