import logging
import secrets

from pydantic import BaseSettings, Field, PostgresDsn, EmailStr, SecretStr

from starlette.datastructures import Secret

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    PROJECT_NAME: str = Field("Spam Predictor with FastAPI", env='PROJECT_NAME')
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    HOST: str = Field('http://127.0.0.1', env="LOCAL_HOST")
    PORT: int = Field(8000, env="LOCAL_PORT")
    BIND_ENV: bool = Field(False, env="BIND")
    use_loglevel: str = Field("debug", env="LOG_LEVEL")

    FIRST_SUPERUSER: str = Field("User Admin", env="FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: SecretStr = Field(..., env="FIRST_SUPERUSER_PASSWORD")
    FIRST_SUPERUSER_EMAIL: EmailStr = Field(..., env="FIRST_SUPERUSER_EMAIL")

    POSTGRES_SERVER: str = Field(env="POSTGRES_SERVER")
    POSTGRES_PORT: str = Field("5432", env="POSTGRES_PORT")
    POSTGRES_USER: str = Field(env="POSTGRES_USER")
    POSTGRES_PASSWORD: SecretStr = Field(env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("spam_ml", env="POSTGRES_DB")

    JWT_SECRET: SecretStr = Field(env="JWT_SECRET")

    class Config:
        case_sensitive = True
        validate_all = True
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()

postgres_pass = settings.POSTGRES_PASSWORD.get_secret_value()
SQLALCHEMY_DATABASE_URI: PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        user=settings.POSTGRES_USER,
        password=postgres_pass,
        port=settings.POSTGRES_PORT,
        host=settings.POSTGRES_SERVER,
        path=f"/{settings.POSTGRES_DB or ''}",
    )


if settings.BIND_ENV:
    print(f"starting: {settings.PROJECT_NAME}")
else:
    use_bind = f"{settings.HOST}:{settings.PORT}"
    print(f"starting: {settings.PROJECT_NAME} on {use_bind}")

print(SQLALCHEMY_DATABASE_URI)
