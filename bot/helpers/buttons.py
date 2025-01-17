from typing import List, Optional, Tuple

from pyrogram import Client
from pyrogram.helpers import ikb
from pyrogram.types import Message

from .handlers import helper_handlers


def admin_buttons() -> ikb:
    buttons = []
    fs_data = helper_handlers.fs_chats
    if fs_data:
        for chat_id in fs_data:
            chat_type = fs_data[chat_id]["chat_type"]
            invite_link = fs_data[chat_id]["invite_link"]
            buttons.append((chat_type, invite_link, "url"))

    button_layouts = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
    button_layouts.append([("ʙᴏᴛ ꜱᴇᴛᴛɪɴɢꜱ", "settings")])

    return ikb(button_layouts)


async def join_buttons(client: Client, message: Message, user_id: int) -> Optional[ikb]:
    no_join_ids = await helper_handlers.user_is_not_join(user_id)
    if not no_join_ids:
        return None

    buttons = []
    fs_data = helper_handlers.fs_chats
    for chat_id in no_join_ids:
        chat_type = fs_data[chat_id]["chat_type"]
        invite_link = fs_data[chat_id]["invite_link"]
        buttons.append((f"Bergabung {chat_type}", invite_link, "url"))

    button_layouts = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]

    if len(message.command) > 1:
        start_url = f"t.me/{client.me.username}?start={message.command[1]}"
        button_layouts.append([("ᴄᴏʙᴀ ʟᴀɢɪ", start_url, "url")])

    return ikb(button_layouts)


class HelperButtons(List[List[Tuple[str, str]]]):
    Close = [[("ᴛᴜᴛᴜᴘ", "close")]]

    Broadcast = [[("ʀᴇꜰʙᴄ", "broadcast refresh"), ("ꜱᴛᴏᴘ", "broadcast stop")]]

    Ping = [[("ʀᴇꜰʀᴇꜱʜ", "ping")]]

    Eval = [[("ʀᴇꜰʀᴇꜱʜ", "eval")]]

    Menu = [
        [("ɢᴇɴᴇʀᴀᴛᴇ ꜱᴛᴀᴛᴜꜱ", "menu generate_status")],
        [("ꜱᴛᴀʀᴛ", "menu start"), ("ꜰᴏʀᴄᴇ", "menu force")],
        [("ᴘʀᴏᴛᴇᴋꜱɪ ᴋᴏɴᴛᴇɴ", "menu protect_content")],
        [("ᴀᴅᴍɪɴ", "menu admins"), ("ꜰꜱᴜʙꜱ", "menu fsubs")],
        [("ᴛᴜᴛᴜᴘ", "close")],
    ]

    Cancel = [[("ʙᴀᴛᴀʟ", "cancel")]]

    Generate = [
        [("« ᴋᴇᴍʙᴀʟɪ", "settings"), ("ᴜʙᴀʜ", "change generate_status")],
        [("ᴛᴜᴛᴜᴘ", "close")],
    ]
    Generate_ = [[("« ᴋᴇᴍʙᴀʟɪ", "menu generate_status"), ["ᴛᴜᴛᴜᴘ", "close"]]]

    Start = [
        [("« ᴋᴇᴍʙᴀʟɪ", "settings"), ("ꜱᴇᴛ", "update start")],
        [("ᴛᴜᴛᴜᴘ", "close")],
    ]
    Start_ = [[("« ᴋᴇᴍʙᴀʟɪ", "menu start"), ("ᴛᴜᴛᴜᴘ", "close")]]

    Force = [
        [("« ᴋᴇᴍʙᴀʟɪ", "settings"), ("ꜱᴇᴛ", "update force")],
        [("ᴛᴜᴛᴜᴘ", "close")],
    ]
    Force_ = [[("« ᴋᴇᴍʙᴀʟɪ", "menu force"), ("ᴛᴜᴛᴜᴘ", "close")]]

    Protect = [
        [("« ᴋᴇᴍʙᴀʟɪ", "settings"), ("ᴜʙᴀʜ", "change protect_content")],
        [("ᴛᴜᴛᴜᴘ", "close")],
    ]
    Protect_ = [[("« ᴋᴇᴍʙᴀʟɪ", "menu protect_content"), ["ᴛᴜᴛᴜᴘ", "close"]]]

    Admins = [
        [("ᴛᴀᴍʙᴀʜᴋᴀɴ", "add admin"), ("ʜᴀᴘᴜꜱ", "del admin")],
        [("« ᴋᴇᴍʙᴀʟɪ", "settings"), ("ᴛᴜᴛᴜᴘ", "close")],
    ]
    Admins_ = [[("« ᴋᴇᴍʙᴀʟɪ", "menu admins"), ("ᴛᴜᴛᴜᴘ", "close")]]

    FSubs = [
        [("ᴛᴀᴍʙᴀʜᴋᴀɴ", "add fsub"), ("ʜᴀᴘᴜꜱ", "del fsub")],
        [("« ᴋᴇᴍʙᴀʟɪ", "settings"), ("ᴛᴜᴛᴜᴘ", "close")],
    ]
    FSubs_ = [[("« ᴋᴇᴍʙᴀʟɪ", "menu fsubs"), ("ᴛᴜᴛᴜᴘ", "close")]]


helper_buttons: HelperButtons = HelperButtons()
