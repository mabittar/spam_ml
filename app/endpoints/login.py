from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user_controller
from app.database.session import get_session
from app.infrastructure.security import verify_password, create_access_token
from app.models import UserSignIn

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/")
async def login(request: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user: UserSignIn = await user_controller.get_by_username(session=session, username=request.username)  # type: ignore
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not verify_password(hashed_password=user.password, plain_password=request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = create_access_token(
        subject=user.email
    )
    # generate JWT token and return
    return {"access_token": access_token, "token_type": "bearer"}
