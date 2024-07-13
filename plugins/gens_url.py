from pyrogram import Client, filters
from pyrogram.helpers import ikb
from pyrogram.types import Message

from bot import authorized_users_only, config, get_generate_status, url_safe

list_available_commands = [
    "batch",
    "broadcast",
    "bc",
    "eval",
    "e",
    "logs",
    "log",
    "ping",
    "p",
    "start",
    "users",
]


@Client.on_message(filters.private & ~filters.command(list_available_commands))
@authorized_users_only
async def generate_handler(client: Client, message: Message) -> None:
    current_generate_status = await get_generate_status()
    if not current_generate_status:
        return

    database_chat_id = config.DATABASE_CHAT_ID
    message_db = await message.copy(database_chat_id)

    encoded_data = url_safe.encode_data(f"id-{message_db.id * abs(database_chat_id)}")
    encoded_data_url = f"https://t.me/{client.me.username}?start={encoded_data}"

    share_encoded_data_url = f"https://t.me/share/url?url={encoded_data_url}"
    await message.reply_text(
        encoded_data_url,
        quote=True,
        reply_markup=ikb([[("Share", share_encoded_data_url, "url")]]),
    )
