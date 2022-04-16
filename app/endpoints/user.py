import logging
from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud.user import user_controller
from app.database.session import get_session
from app.endpoints.login import get_current_user
from app.models.usermodel import UserModel
from app.models import UserSignOut, UserSignIn, BaseUser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Users"], prefix="/users")


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


@router.get("/whoami", status_code=status.HTTP_200_OK, response_model=UserSignOut)
async def who_am_i(
        current_user: UserModel = Depends(get_current_user)):
    logger.info("Who am I endpoint")
    response = UserSignOut(
        document_number=current_user.document_number,
        email=current_user.email,
        full_name=current_user.full_name,
        username=current_user.username,
        created_at=current_user.created_at,
        id=current_user.id,
        phone=current_user.phone
    )
    return response



