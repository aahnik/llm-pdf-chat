# background tasks

from crud import create_new_msg
from models import Message
import lang


async def generate_response(prompt: str):
    llm_response = lang.chain(prompt)
    await create_new_msg(Message(username="assistant", message=llm_response["result"]))
