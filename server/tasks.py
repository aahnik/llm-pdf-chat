# background tasks
import time
from crud import create_new_msg
from models import Message

import asyncio


async def generate_response(prompt: str):
    await asyncio.sleep(10)
    await create_new_msg(Message(username="assistant", message=f"Response to {prompt}"))