from pyrogram import Client, filters
from pyrogram.types import Message, User

from bot import admin_buttons, config, helper_handlers, join_buttons
from bot.db_funcs import (
    add_user,
    get_force_text_msg,
    get_protect_content,
    get_start_text_msg,
)


@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client: Client, message: Message) -> None:
    user = message.from_user
    await add_user(user.id)

    user_buttons = await join_buttons(client, message, user.id)
    if len(message.command) == 1:
        start_text = await get_start_text_msg()
        start_text = format_text_message(start_text, user)
        if user.id not in helper_handlers.admins:
            await message.reply_text(start_text, quote=True, reply_markup=user_buttons)
        else:
            buttons = admin_buttons()
            await message.reply_text(start_text, quote=True, reply_markup=buttons)
        return
    else:
        force_text = await get_force_text_msg()
        force_text = format_text_message(force_text, user)
        if await helper_handlers.user_is_not_join(user.id):
            await message.reply_text(force_text, quote=True, reply_markup=user_buttons)
            return

    message_ids = helper_handlers.decode_data(message.command[1])

    msgs = await client.get_messages(config.DATABASE_CHAT_ID, message_ids)
    for msg in msgs:
        if msg.empty:
            pass

        protect_content = await get_protect_content()
        await msg.copy(user.id, protect_content=protect_content)


def format_text_message(text: str, user: User) -> str:
    first_name, last_name = user.first_name, user.last_name
    full_name = f"{first_name} {last_name}".strip() if last_name else first_name
    return text.format(
        first_name=first_name,
        last_name=last_name,
        full_name=full_name,
        mention=user.mention(full_name),
    )
