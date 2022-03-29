from sqlalchemy import select
from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Security
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

import crud
import models
from crud.user.user import user
from database.session import get_db
from models.user import User
from settings import SECRET_KEY, PROJECT_NAME
from infrastructure.security import get_password_hash, create_access_token
from models import UserSignOut, UserSignIn, BaseUser
from models.token import TokenPayload

router = APIRouter()


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{PROJECT_NAME}/login/access-token"
)


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.user:
    try:
        payload = jwt.decode(
            token, str(SECRET_KEY), algorithms=[Security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post(
    "/register/",
    response_model=UserSignOut,
    status_code=201
    )
async def create_user(
        user_in: UserSignIn,
        session: AsyncSession = Depends(get_db)
) -> Any:
    """
        Create new user.
        """
    user_db = await session.execute(select(User).where(User.email == user_in.email))
    if user_db:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user_db.password = get_password_hash(user.password)

    created_user = await user.create(session, obj_in=user_in)
    token = create_access_token(created_user)
    response = UserSignOut(
        full_name=created_user["full_name"],
        email=created_user["email"],
        phone=created_user["phone"],
        created_at=created_user["created_at"],
        last_modified_at=created_user["last_modified_at"],
        role=created_user["role"],
        token=token
    )
    return response


@router.get("/", response_model=List[BaseUser])
def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    listed_users = user.get_multi(db, skip=skip, limit=limit)
    return listed_users


