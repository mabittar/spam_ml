import logging
from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Security
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from app.crud.user import user_controller
from app.database.session import get_session
from app.models.user import User
from app.settings import settings
from app.infrastructure.security import create_access_token
from app.models import UserSignOut, UserSignIn, BaseUser
from app.models.token import TokenPayload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Users"], prefix="/users")


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.PROJECT_NAME}/login/access-token"
)


def get_current_user(
        db: Session = Depends(get_session), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        logger.info("Get current user")
        payload = jwt.decode(
            token, str(settings.SECRET_KEY), algorithms=[Security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_db = user_controller.get(db, id=token_data.sub)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db


@router.post(
    "/register/",
    response_model=UserSignOut,
    status_code=status.HTTP_201_CREATED
    )
async def create_user(
        user_in: UserSignIn,
        session: AsyncSession = Depends(get_session)
) -> Any:
    """
        Create new user.
        """
    logger.info("Register new user")
    user_db = await user_controller.get_by_email(session=session, email=user_in.email)
    if user_db:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    logger.info("Creating new user")

    created_user = await user_controller.create(session, obj_in=user_in)
    await session.commit()
    await session.refresh(created_user)
    response = UserSignOut(
        id=created_user.id,
        full_name=created_user.full_name,
        email=created_user.email,
        phone=created_user.phone,
        created_at=created_user.created_at,
        document_number=created_user.document_number,
        username=created_user.username
    )
    logger.info("Returning user created")
    return response


@router.get("/", response_model=List[BaseUser])
async def read_users(
    db: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 30,
) -> Any:
    """
    Retrieve users.
    """
    logger.info("Get listed users")
    listed_users = await user_controller.get_multi(db, skip=skip, limit=limit)
    return listed_users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserSignOut)
async def get_user_by_id(_id: int, session: AsyncSession = Depends(get_session)):
    logger.info("Get user by id")
    return await user_controller.get(session=session, id=_id)



