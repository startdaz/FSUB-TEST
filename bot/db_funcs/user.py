from typing import List

from ..base import database
from ..utils import BOT_ID


async def add_user(user_id: int) -> None:
    await database.add_value(int(BOT_ID), "BOT_USERS", user_id)


async def del_user(user_id: int) -> None:
    await database.del_value(int(BOT_ID), "BOT_USERS", user_id)


async def get_users() -> List[int]:
    doc = await database.get_doc(int(BOT_ID))
    return doc.get("BOT_USERS", [])
