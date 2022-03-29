import logging
import secrets
from starlette.config import Config

from starlette.datastructures import Secret

logger = logging.getLogger(__name__)


config = Config(".env")

PROJECT_NAME: str = config("PROJECT_NAME", cast=str, default="Spam Predictor with FastAPI")
SECRET_KEY: str = secrets.token_urlsafe(32)
# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

HOST: str = config("LOCAL_HOST", cast=str, default='http://127.0.0.1')
PORT: int = config("LOCAL_PORT", cast=int, default=8000)
bind_env = config("BIND", cast=bool, default=False)
use_loglevel = config("LOG_LEVEL", default="info")
if bind_env:
    use_bind = bind_env
    print(f"starting: {PROJECT_NAME}")
else:
    use_bind = f"{HOST}:{PORT}"
    print(f"starting: {PROJECT_NAME} on {use_bind}")

FIRST_SUPERUSER: str = config("FIRST_SUPERUSER", cast=str, default="User Admin")
FIRST_SUPERUSER_PASSWORD = config("FIRST_SUPERUSER_PASSWORD", cast=Secret)
FIRST_SUPERUSER_EMAIL: str = config("FIRST_SUPERUSER_EMAIL", cast=str)

POSTGRES_SERVER: str = config("POSTGRES_SERVER", cast=str, default="l")
POSTGRES_PORT: str = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_USER: str = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_DB = config("POSTGRES_DB", cast=str)


JWT_SECRET = config("JWT_SECRET", cast=Secret)



