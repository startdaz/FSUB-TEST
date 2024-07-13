from ..base import database
from ..utils import BOT_ID


async def add_force_text_msg(value: str) -> None:
    await database.add_value(int(BOT_ID), "FORCE_TEXT", value)


async def del_force_text_msg() -> None:
    await database.clear_value(int(BOT_ID), "FORCE_TEXT")


async def get_force_text_msg() -> str:
    doc = await database.get_doc(int(BOT_ID))
    return doc.get("FORCE_TEXT", [])[0]


async def update_force_text_msg(value: str) -> None:
    await del_force_text_msg()
    await add_force_text_msg(value)


async def add_start_text_msg(value: str) -> None:
    await database.add_value(int(BOT_ID), "START_TEXT", value)


async def del_start_text_msg() -> None:
    await database.clear_value(int(BOT_ID), "START_TEXT")


async def get_start_text_msg() -> str:
    doc = await database.get_doc(int(BOT_ID))
    return doc.get("START_TEXT", [])[0]


async def update_start_text_msg(value: str) -> None:
    await del_start_text_msg()
    await add_start_text_msg(value)
