from datetime import datetime, timedelta
from traceback import format_exc
from typing import Any, Union

from fastapi import HTTPException, status

from app.settings import settings
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt", "des_crypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception:
        str_tb = format_exc()
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=str_tb)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
