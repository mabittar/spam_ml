from datetime import datetime
from typing import Union
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models import UserModel
from app.models import PredictionModel, SpamResponse, SpamRequest


class CRUDPrediction(CRUDBase[PredictionModel, SpamRequest, SpamResponse]):
    @staticmethod
    async def get_used_by_month(session: AsyncSession, user_id: int) -> Union[int, None]:
        today = datetime.now()

        query = select(PredictionModel).where(PredictionModel.owner_id == user_id)
        query = query.where(PredictionModel.created_at.month == today.month)
        result = await session.execute(query)
        result = result.count()
        return result

    async def save_prediction(self, session: AsyncSession, *, user: UserModel, text_message: str, result: bool) -> PredictionModel:
        db_obj = PredictionModel(
            prediction_key=str(uuid4()), # noqa
            text_message=text_message, # noqa
            predictin=result, # noqa
            user=user, # noqa
            created_at=datetime.now() # noqa
        )
        session.add(db_obj)
        await session.flush()
        return db_obj


prediction_controller = CRUDPrediction(PredictionModel)
