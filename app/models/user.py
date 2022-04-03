import logging
from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
import enum
import sqlalchemy
from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy import Column, String, DateTime, Enum, Integer

from app.database.base_class import Base
from app.utils.document_validator import parse_doc_number

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class User(Base):
    id: Column(Integer, primary_key=True, autoincrement=True, index=True)
    email: str = Column(String(120), unique=True, index=True, nullable=False)
    password: str = Column(String(255), nullable=False)
    full_name: str = Column(String(200))
    username: str = Column(String(200), index=True, unique=True, nullable=False)
    document_number: str = Column(String(14), nullable=False, unique=True)
    phone: str = Column(String(13), nullable=True)
    created_at: datetime = Column(DateTime, nullable=False, server_default=sqlalchemy.func.now())
    # TODO: fix migrations/vversions to handle with enum column
    # role: str = Column(Enum("super_admin", "admin", "user", name="user_role", create_type=False), nullable=False, default="user")

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


class FullNameField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> str:
        try:
            first_name, *last_name = v.split()
            if len(last_name) == 0 or last_name is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    detail="Full Name must be at least two names")
            return f"{last_name[-1].capitalize()}, {first_name.capitalize()}"
        except Exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="Full Name must be at least two names")


class UserRole(enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    user = "user"


class BaseUser(BaseModel):
    email: EmailStr = Field(..., description="User email for contact")
    full_name: FullNameField = Field(min_length=3)
    document_number: str = Field(..., description="User document number")

    @validator("full_name")
    def validate_full_name(cls, v):
        try:
            first_name, *last_name = v.split()
            return v
        except Exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="You should provide at least 2 names")

    @validator("document_number")
    def validate_document_number(cls, v):
        try:
            logger.info(f"Validating document number {v}")
            return parse_doc_number(v)
        except Exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail="You should provide a valid document number")


class UserSignIn(BaseUser):
    password: str = Field(min_length=6, description="User Password")
    username: str = Field(..., min_length=3,  description="Username to login")
    # role: Optional[str]
    phone: Optional[str]

    class Config:
        orm_mode = True


class UserSignOut(BaseUser):
    id: int
    created_at: datetime
    # role: UserRole
    phone: Optional[str]
    username: str
