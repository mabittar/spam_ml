from datetime import datetime
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database.base_class import Base

if TYPE_CHECKING:
    from .user_model import UserModel # noqa


class PredictionModel(Base):
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    prediction_key: str = Column(String(36), unique=True, nullable=False)
    text_message: str = Column(String(360), nullable=False)
    prediction: int = Column(Integer)
    owner_id = Column(Integer, ForeignKey("usermodel.id"))

    owner = relationship(
        "UserModel", back_populates="predictions"
    )
    created_at: datetime = Column(DateTime, index=True, nullable=False, server_default=func.now())

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


class SpamRequest(BaseModel):
    text_message: str


class SpamResponse(SpamRequest):
    spam_polarity: str
    month_used_amount: Optional[int]
