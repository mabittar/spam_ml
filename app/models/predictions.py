from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database.base_class import Base
from app.models import UserModel


class PredictionModel(Base):
    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    prediction_key: str = Column(String(36), unique=True, nullable=False)
    text_message: str = Column(String(360), unique=True, nullable=False)
    prediction: int = Column(Integer)
    user_id: Column(String, ForeignKey(UserModel.id), nullable=False, index=True)
    # user = relationship(
    #     "UserModel", foreign_keys=[user_id], lazy="joined"
    # )
    created_at: datetime = Column(DateTime, index=True, nullable=False, server_default=func.now())



class SpamRequest(BaseModel):
    text_message: str


class SpamResponse(SpamRequest):
    spam_polarity: str
    month_used_amount: Optional[int]
