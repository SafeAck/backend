"""
Contains common schemas used across the application
"""

from pydantic import BaseModel


class ResponseSchema(BaseModel):
    """basic Response Schema for returning response"""

    msg: str
    data: dict | None
    status_code: int = 200
