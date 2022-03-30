from datetime import datetime
from typing import Optional

import enum
import sqlalchemy
from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy import Column, String, DateTime, Enum, Integer

from app.database.base_class import Base


class User(Base):
    id: Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(120), unique=True)
    password: str = Column(String(255))
    full_name: str = Column(String(200))
    phone: str = Column(String(13), nullable=True)
    created_at: datetime = Column(DateTime, nullable=False, server_default=sqlalchemy.func.now())
    role: str = Column(Enum("super_admin", "admin", "user"), nullable=False, default="user")


class FullNameField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> str:
        try:
            first_name, *last_name = v.split()
            if len(last_name) == 0 or last_name is None:
                raise ValueError("Full Name must be at least two names")
            return f"{last_name[-1].capitalize()}, {first_name.capitalize()}"
        except:
            raise ValueError("Full Name must be at least two names")


class UserRole(enum.Enum):
    super_admin = "super admin"
    admin = "admin"
    user = "user"


class BaseUser(BaseModel):
    email: EmailStr = Field(..., description="User email for contact")
    full_name: FullNameField = Field(min_length=3)

    @validator("full_name")
    def validate_full_name(cls, v):
        try:
            first_name, last_name = v.split()
            return v
        except Exception:
            raise ValueError("You should provide at least 2 names")


class UserSignIn(BaseUser):
    password: str = Field(min_length=6, description="User Password")
    role: Optional[str]

    class Config:
        orm_mode = True


class UserSignOut(BaseUser):
    phone: Optional[str]
    created_at: datetime
    last_modified_at: datetime
    token: str
    role: UserRole
