import logging
from typing import Any

from app.infrastructure.security import ALGORITHM
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose.jwt import decode, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.settings import settings
from app.models.token import TokenPayload

from app.crud import user_controller
from app.database.session import get_session
from app.infrastructure.security import verify_password, create_access_token
from app.models import UserSignIn, UserModel, UserSignOut
from app.models.token import Token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/login", tags=["Authentication"])


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={
        "test_token": "Token tests",
        "spam_ml": "Use machine learning endpoint",
    }
)


async def get_current_user(
        security_scopes: SecurityScopes,
        token: str = Depends(reusable_oauth2),
        db: Session = Depends(get_session),
) -> UserModel:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        logger.info("Get current user")
        payload = decode(
            token,
            str(settings.SECRET_KEY),
            algorithms=[ALGORITHM]
        )

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenPayload(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user_db = await user_controller.get_by_username(db, username=username)
    if not user_db:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user_db


@router.post("/", response_model=Token)
async def login(
        request: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    user: UserSignIn = await user_controller.authenticate(
        session=session,
        username=request.username,
        password=request.password
    )  # type: ignore
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")

    logging.debug("generate  JWT token")
    access_token = create_access_token(
        data={"sub": user.username, "scopes": request.scopes}
    )
    response = Token(access_token=access_token, token_type="bearer")
    return response


@router.post("/test_token")
def test_token(user: UserModel = Security(get_current_user, scopes=["test_token"])) -> Any:
    logging.info("test access token")
    return {"message": "valid token"}
