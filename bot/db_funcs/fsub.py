from typing import List, Optional

from ..base import database
from ..utils import BOT_ID


async def add_fs_chat(chat_id: int) -> None:
    await database.add_value(int(BOT_ID), "FSUB_CHATS", chat_id)


async def del_fs_chat(chat_id: int) -> None:
    await database.del_value(int(BOT_ID), "FSUB_CHATS", chat_id)


async def get_fs_chats() -> Optional[List[int]]:
    doc = await database.get_doc(int(BOT_ID))

    return doc.get("FSUB_CHATS", [])
