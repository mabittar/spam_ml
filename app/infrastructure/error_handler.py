from typing import Optional, Union

from pydantic import BaseModel


class ErrorMessage(BaseModel):
    title: Optional[str]
    traceback: Optional[str]
    code: Optional[str] = ""
