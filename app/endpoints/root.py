import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["root"])


@router.get("/")
async def root(session: AsyncSession = Depends(get_session)):
    Settings()
    try:
        # Try to create session to check if DB is awake
        await session.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e

    return {"message": "Wellcome to FastAPI Machine Learning Spam Predictor"}


