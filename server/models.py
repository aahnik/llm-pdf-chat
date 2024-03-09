from typing import Annotated

from beanie import Document, Indexed
from pydantic import BaseModel


class Message(BaseModel):
    username: str
    message: str


class Messages(Document, Message):
    seqno: Annotated[int, Indexed()]


class LLMConfig(Document):
    uid: Annotated[int, Indexed()]
    model: str
    temperature: float
