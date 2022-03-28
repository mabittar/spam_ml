from typing import Optional, Union

from pydantic import BaseModel


class ErrorMessage(BaseModel):
    title: Optional[str]
    traceback: Optional[str]
    http_status: int
    code: Optional[str] = ""
