# background tasks

import traceback

import lang
from crud import create_new_msg
from models import Message


async def generate_response(prompt: str):
    try:
        llm_response = await lang.chain.acall(prompt)
    except Exception as err:
        print("".join(traceback.format_exception(err)))

        message = f"Sorry... There was some error unfortunately.\n```text\n{type(err)}\n{str(err)}\n```"
    else:
        message = llm_response["result"]
    finally:
        await create_new_msg(Message(username="assistant", message=message))
