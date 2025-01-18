from typing import Optional

from pyrogram import Client, errors, filters
from pyrogram.helpers import ikb
from pyrogram.types import Message

from bot import authorized_users_only, config, url_safe


@Client.on_message(filters.private & filters.command("batch"))
@authorized_users_only
async def batch_handler(client: Client, message: Message) -> None:
    database_chat_id = config.DATABASE_CHAT_ID

    ask_text = "ᴛᴇʀᴜꜱᴋᴀɴ ᴘᴇꜱᴀɴ ᴅᴀʀɪ ᴄʜᴀɴɴᴇʟ ᴅᴀᴛᴀʙᴀꜱᴇ\n\n ᴡᴀᴋᴛᴜ ʜᴀʙɪꜱ: 30 ᴅᴇᴛɪᴋ"
    first_message = await ask_helper_func(client, message, ask_text)
    if not first_message:
        return

    first_id = first_message * abs(database_chat_id)

    last_message = await ask_helper_func(client, message, ask_text)
    if not last_message:
        return

    last_id = last_message * abs(database_chat_id)

    encoded_data = url_safe.encode_data(f"id-{first_id}-{last_id}")
    encoded_data_url = f"https://t.me/{client.me.username}?start={encoded_data}"

    share_encoded_data_url = f"https://t.me/share?url={encoded_data_url}"
    await message.reply_text(
        encoded_data_url,
        reply_markup=ikb([[("Share", share_encoded_data_url, "url")]]),
    )


async def ask_helper_func(
    client: Client, message: Message, ask_text: str
) -> Optional[int]:
    chat_id, user_id = message.chat.id, message.from_user.id
    config.DATABASE_CHAT_ID

    ask_message = None
    try:
        ask_message = await client.ask(
            chat_id=chat_id,
            text=ask_text,
            user_id=user_id,
            timeout=30,
        )
    except errors.ListenerTimeout:
        await message.reply_text("ʙᴀᴛᴀꜱ ᴡᴀᴋᴛᴜ ᴛᴇʀᴄᴀᴘᴀɪ!\n ᴘʀᴏꜱᴇꜱ ᴛᴇʟᴀʜ ᴅɪʙᴀᴛᴀʟᴋᴀɴ")
        return

    if (
        not ask_message.forward_from_chat
        or ask_message.forward_from_chat.id != config.DATABASE_CHAT_ID
    ):
        await ask_message.reply_text(
            "<i>ᴘᴇꜱᴀɴ ᴛɪᴅᴀᴋ ᴠᴀʟɪᴅ!\n ᴛᴇʀᴜꜱᴋᴀɴ ꜱᴀᴊᴀ ᴘᴇꜱᴀɴ ᴅᴀʀɪ ᴄʜᴀɴɴᴇʟ ᴅᴀᴛᴀʙᴀꜱᴇ</i>",
            quote=True,
        )
        return

    return ask_message.forward_from_message_id
