from pydantic import BaseModel
from beanie import Document, Indexed
from typing import Annotated


class Message(BaseModel):
    username: str
    message: str


class Messages(Document, Message):
    seqno: Annotated[int, Indexed()]
