import logging
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.user import user_controller
from app.database.session import get_session
from app.models import UserSignIn
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init_db(db: Session = Depends(get_session)) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    first_pass = settings.FIRST_SUPERUSER_PASSWORD.get_secret_value()
    user_db = await user_controller.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user_db:
        user_in = UserSignIn(
            full_name=settings.FIRST_SUPERUSER,  # type: ignore
            password=first_pass,
            role="super admin",
            email=settings.FIRST_SUPERUSER_EMAIL,  # type: ignore
            document_number="98765432100"
        )
        await user_controller.create(db, obj_in=user_in)

        return user_in
