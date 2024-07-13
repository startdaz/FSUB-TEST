from ..base import database
from ..utils import BOT_ID


async def add_generate_status(value: bool) -> None:
    await database.add_value(int(BOT_ID), "GENERATE_URL", value)


async def del_generate_status() -> None:
    await database.clear_value(int(BOT_ID), "GENERATE_URL")


async def get_generate_status() -> bool:
    doc = await database.get_doc(int(BOT_ID))
    return doc.get("GENERATE_URL", [])[0]


async def update_generate_status() -> None:
    current_generate_status = await get_generate_status()
    await del_generate_status()
    await add_generate_status(not current_generate_status)


async def add_protect_content(value: bool) -> None:
    await database.add_value(int(BOT_ID), "PROTECT_CONTENT", value)


async def del_protect_content() -> None:
    await database.clear_value(int(BOT_ID), "PROTECT_CONTENT")


async def get_protect_content() -> bool:
    doc = await database.get_doc(int(BOT_ID))
    return doc.get("PROTECT_CONTENT", [])[0]


async def update_protect_content() -> None:
    protect_content_status = await get_protect_content()
    await del_protect_content()
    await add_protect_content(not protect_content_status)
