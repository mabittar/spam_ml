from datetime import datetime
from typing import Optional

import enum
import sqlalchemy
from pydantic import BaseModel, EmailStr, Field, validator

from database.session import metadata


class UserRole(enum.Enum):
    super_admin = "super admin"
    admin = "admin"
    user = "user"


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(120), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
    sqlalchemy.Column("full_name", sqlalchemy.String(200)),
    sqlalchemy.Column("phone", sqlalchemy.String(13)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("role", sqlalchemy.Enum(UserRole), nullable=False, server_default=UserRole.user.name)
)


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


class UserSignOut(BaseUser):
    phone: Optional[str]
    created_at: datetime
    last_modified_at: datetime
    token: str
    role: UserRole
