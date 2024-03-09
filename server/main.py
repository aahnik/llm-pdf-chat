from typing import List

from beanie import init_beanie
from config import CONFIG
from crud import create_new_msg
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Message, Messages
from motor.motor_asyncio import AsyncIOMotorClient
from tasks import generate_response

description = """
Multi Chat with LLMs
"""

app = FastAPI(title="LLM chat API", version="0.0.1", description=description)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_app():
    client = AsyncIOMotorClient(CONFIG.mongo_uri)
    db = client[CONFIG.db_name]
    await init_beanie(
        database=db,
        document_models=[Messages],
    )


@app.get("/messages/{offset}")
async def get_messages(offset: int = 0) -> List[Messages]:
    return await Messages.find(Messages.seqno > offset).to_list()


@app.post("/messages/")
async def post_message(message: Message, bg: BackgroundTasks) -> Message:
    msg = await create_new_msg(message)
    bg.add_task(generate_response, prompt=message.message)
    return msg
