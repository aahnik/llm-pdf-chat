from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from models import Message, Messages
from config import CONFIG
from typing import List


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
async def post_message(message: Message) -> Message:
    last_msgs = await Messages.find().sort(-Messages.seqno).limit(1).to_list()
    if last_msgs:
        new_seqno = last_msgs[0].seqno + 1
    else:
        new_seqno = 0
    new_msg = await Messages.create(
        Messages(seqno=new_seqno, username=message.username, message=message.message)
    )
    return await new_msg.save()
