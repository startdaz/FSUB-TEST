from ..base import database
from ..utils import BOT_ID


async def add_restart_data_id(chat_id: int, message_id: int) -> None:
    await del_restart_data_id()

    restart_data = {"chat_id": chat_id, "message_id": message_id}
    await database.add_value(int(BOT_ID), "RESTART_IDS", restart_data)


async def del_restart_data_id():
    await database.clear_value(int(BOT_ID), "RESTART_IDS")


async def get_restart_data_ids():
    doc = await database.get_doc(int(BOT_ID))
    return doc.get("RESTART_IDS")[0]
