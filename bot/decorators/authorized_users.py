import functools
from typing import Callable, Union

from pyrogram import Client
from pyrogram.types import CallbackQuery, Message

from ..helpers import helper_handlers


def authorized_users_only(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(client: Client, event: Union[Message, CallbackQuery]) -> None:
        if event.from_user.id not in helper_handlers.admins:
            if isinstance(event, Message):
                pass
            elif isinstance(event, CallbackQuery):
                await event.answer("ʙᴜᴋᴀɴ ᴍɪʟɪᴋᴍᴜ!", show_alert=True)
            return

        await func(client, event)

    return wrapper
