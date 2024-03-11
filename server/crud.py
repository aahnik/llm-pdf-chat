from models import Message, Messages, LLMConfig


async def create_new_msg(message: Message):
    last_msgs = await Messages.find().sort(-Messages.seqno).limit(1).to_list()
    if last_msgs:
        new_seqno = last_msgs[0].seqno + 1
    else:
        new_seqno = 0
    new_msg = await Messages.create(
        Messages(seqno=new_seqno, username=message.username, message=message.message)
    )
    return await new_msg.save()


async def get_llm_config() -> LLMConfig:
    cfg = await LLMConfig.find_one(LLMConfig.uid == 0)
    return cfg.model, cfg.temperature


async def set_llm_config(model: str, temperature: float):
    cfg = await LLMConfig.find_one(LLMConfig.uid == 0)
    cfg.model = model
    cfg.temperature = temperature
    await cfg.save()


async def init_llm_config():
    cfg = await LLMConfig.find_one(LLMConfig.uid == 0)
    if not cfg:
        cfg = LLMConfig(uid=0, model="claude-2", temperature=0.2)
        await cfg.create()
