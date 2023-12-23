from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Error(BaseModel):
    message: str


class MessageIn(BaseModel):
    recipient: int
    sender: int
    content: str


class MessageOut(BaseModel):
    id: int
    recipient: int
    sender: int
    content: str
    date: datetime
    is_read: Optional[bool] = False
    username: str
    profile_image: Optional[str]
    profile_link: Optional[str]
    user_id: int
