
from pydantic import BaseModel


class SpamRequest(BaseModel):
    text_message: str


class SpamResponse(SpamRequest):
    spam_polarity: str