from pyrogram import Client, filters
from pyrogram.types import Message

from bot import authorized_users_only, get_users


@Client.on_message(filters.private & filters.command("users"))
@authorized_users_only
async def users_handler(_, message: Message) -> None:
    counting_message = await message.reply_text("ᴍᴇɴɢʜɪᴛᴜɴɢ...", quote=True)

    total_users = await get_users()
    await counting_message.edit_text(f"<code>{len(total_users)}</code> ᴘᴇɴɢɢᴜɴᴀ")
