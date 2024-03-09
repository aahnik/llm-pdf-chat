from models import Message, Messages


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
