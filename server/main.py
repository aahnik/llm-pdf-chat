from typing import List

from beanie import init_beanie
from config import CONFIG
from crud import create_new_msg, init_llm_config, set_llm_config
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lang import load_chain, process_docs
from models import LLMConfig, Message, Messages
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
        document_models=[Messages, LLMConfig],
    )
    await init_llm_config()
    await process_docs()
    await load_chain()


@app.get("/messages/{offset}")
async def get_messages(offset: int = 0) -> List[Messages]:
    return await Messages.find(Messages.seqno > offset).to_list()


@app.post("/messages/")
async def post_message(message: Message, bg: BackgroundTasks) -> Message:
    msg = await create_new_msg(message)
    bg.add_task(generate_response, prompt=message.message)
    return msg


@app.post("/process_pdfs/")
async def process_pdfs():
    try:
        await process_docs()
        await load_chain()
        return {"message": "success"}
    except Exception as err:
        return {"error": str(err)}


@app.post("/set_llm/")
async def set_llm(model: str, temperature: float):
    try:
        await set_llm_config(model, temperature)
        await load_chain()
        return {"message": "success"}
    except Exception as err:
        return {"error": str(err)}
