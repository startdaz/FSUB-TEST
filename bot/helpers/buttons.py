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
    button_layouts.append([("Bot Settings", "settings")])

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
        buttons.append((f"Join {chat_type}", invite_link, "url"))

    button_layouts = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]

    if len(message.command) > 1:
        start_url = f"t.me/{client.me.username}?start={message.command[1]}"
        button_layouts.append([("Try Again", start_url, "url")])

    return ikb(button_layouts)


class HelperButtons(List[List[Tuple[str, str]]]):
    Close = [[("Close", "close")]]

    Broadcast = [[("Ref", "broadcast refresh"), ("Stop", "broadcast stop")]]

    Ping = [[("Refresh", "ping")]]

    Eval = [[("Refresh", "eval")]]

    Menu = [
        [("Generate Status", "menu generate_status")],
        [("Start", "menu start"), ("Force", "menu force")],
        [("Protect Content", "menu protect_content")],
        [("Admins", "menu admins"), ("FSubs", "menu fsubs")],
        [("Close", "close")],
    ]

    Cancel = [[("Cancel", "cancel")]]

    Generate = [
        [("« Back", "settings"), ("Change", "change generate_status")],
        [("Close", "close")],
    ]
    Generate_ = [[("« Back", "menu generate_status"), ["Close", "close"]]]

    Start = [
        [("« Back", "settings"), ("Set", "update start")],
        [("Close", "close")],
    ]
    Start_ = [[("« Back", "menu start"), ("Close", "close")]]

    Force = [
        [("« Back", "settings"), ("Set", "update force")],
        [("Close", "close")],
    ]
    Force_ = [[("« Back", "menu force"), ("Close", "close")]]

    Protect = [
        [("« Back", "settings"), ("Change", "change protect_content")],
        [("Close", "close")],
    ]
    Protect_ = [[("« Back", "menu protect_content"), ["Close", "close"]]]

    Admins = [
        [("Add", "add admin"), ("Delete", "del admin")],
        [("« Back", "settings"), ("Close", "close")],
    ]
    Admins_ = [[("« Back", "menu admins"), ("Close", "close")]]

    FSubs = [
        [("Add", "add fsub"), ("Delete", "del fsub")],
        [("« Back", "settings"), ("Close", "close")],
    ]
    FSubs_ = [[("« Back", "menu fsubs"), ("Close", "close")]]


helper_buttons: HelperButtons = HelperButtons()
