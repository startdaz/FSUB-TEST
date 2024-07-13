from typing import List

from pyrogram import Client, errors, filters
from pyrogram.enums import ChatType
from pyrogram.helpers import ikb
from pyrogram.types import CallbackQuery

from bot import (
    add_admin,
    add_fs_chat,
    authorized_users_only,
    del_admin,
    del_fs_chat,
    get_admins,
    get_force_text_msg,
    get_fs_chats,
    get_generate_status,
    get_protect_content,
    get_start_text_msg,
    helper_buttons,
    helper_handlers,
    logger,
    update_force_text_msg,
    update_generate_status,
    update_protect_content,
    update_start_text_msg,
)


@Client.on_callback_query(filters.regex(r"^cancel$"))
@authorized_users_only
async def cancel_handler_query(client: Client, query: CallbackQuery) -> None:
    chat_id, user_id = query.message.chat.id, query.from_user.id
    await client.stop_listening(chat_id=chat_id, user_id=user_id)


@Client.on_callback_query(filters.regex(r"^settings$"))
@authorized_users_only
async def settings_handler_query(_, query: CallbackQuery) -> None:
    await query.message.edit_text(
        "<b>Bot Settings:</b>", reply_markup=ikb(helper_buttons.Menu)
    )


@Client.on_callback_query(filters.regex(r"^close$"))
@authorized_users_only
async def close_handler_query(_, query: CallbackQuery) -> None:
    try:
        await query.message.reply_to_message.delete()
    except errors.RPCError:
        pass

    await query.message.delete()


@Client.on_callback_query(filters.regex(r"^menu"))
@authorized_users_only
async def menu_handler_query(_, query: CallbackQuery) -> None:
    def format_list_items(item_title: str, list_items: List[int]) -> str:
        if list_items:
            format_items = "".join(
                f"  {i + 1}. <code>{item}</code>\n" for i, item in enumerate(list_items)
            )
        else:
            format_items = "  <code>None</code>"
        return f"{item_title}:\n{format_items}"

    query_data = query.data.split()[1]
    if query_data == "generate_status":
        current_status = await get_generate_status()
        await query.message.edit_text(
            f"Currently Generate Status is <b>{current_status}</b>",
            reply_markup=ikb(helper_buttons.Generate),
        )
    elif query_data == "start":
        current_text = await get_start_text_msg()
        await query.message.edit_text(
            f"<b>Start Text:</b>\n  {current_text}",
            reply_markup=ikb(helper_buttons.Start),
        )
    elif query_data == "force":
        current_text = await get_force_text_msg()
        await query.message.edit_text(
            f"<b>Force Text:</b>\n  {current_text}",
            reply_markup=ikb(helper_buttons.Force),
        )
    elif query_data == "protect_content":
        current_status = await get_protect_content()
        await query.message.edit_text(
            f"Currently Protect Content is <b>{current_status}</b>",
            reply_markup=ikb(helper_buttons.Protect),
        )
    elif query_data == "admins":
        list_admins = await get_admins()
        list_admins = format_list_items("<b>List Admins</b>", list_admins)
        await query.message.edit_text(
            list_admins, reply_markup=ikb(helper_buttons.Admins)
        )
    elif query_data == "fsubs":
        list_fsubs = await get_fs_chats()
        list_fsubs = format_list_items("<b>List FSubs</b>", list_fsubs)
        await query.message.edit_text(
            list_fsubs, reply_markup=ikb(helper_buttons.FSubs)
        )


@Client.on_callback_query(filters.regex(r"^change"))
@authorized_users_only
async def change_handler_query(_, query: CallbackQuery) -> None:
    query_data = query.data.split()[1]
    if query_data == "generate_status":
        await update_generate_status()
        current_status = await get_generate_status()
        await query.message.edit_text(
            f"Generate Status has been changed to <b>{current_status}</b>",
            reply_markup=ikb(helper_buttons.Generate_),
        )
    elif query_data == "protect_content":
        await update_protect_content()
        current_status = await get_protect_content()
        await query.message.edit_text(
            f"Protect Content has been changed to <b>{current_status}</b>",
            reply_markup=ikb(helper_buttons.Protect_),
        )


@Client.on_callback_query(filters.regex(r"^update"))
@authorized_users_only
async def set_handler_query(client: Client, query: CallbackQuery) -> None:
    query_data = query.data.split()[1]
    chat_id, user_id = query.message.chat.id, query.from_user.id

    data = "start" if query_data == "start" else "force"
    await query.message.edit_text(
        f"Send a new {data} text message",
        reply_markup=ikb(helper_buttons.Cancel),
    )

    new_text = None
    buttons = (
        ikb(helper_buttons.Start_)
        if query_data == "start"
        else ikb(helper_buttons.Force_)
    )
    try:
        listening = await client.listen(chat_id=chat_id, user_id=user_id)
        new_text = listening.text
        await listening.delete()
    except errors.ListenerStopped:
        await query.message.edit_text(
            "Process has been cancelled!", reply_markup=buttons
        )
        return

    if not new_text:
        await query.message.edit_text(
            "Invalid! Just send a text message", reply_markup=buttons
        )
    else:
        if query_data == "start":
            await update_start_text_msg(new_text)
        else:
            await update_force_text_msg(new_text)

        await query.message.edit_text(
            f"New {data} text message:\n  {new_text}", reply_markup=buttons
        )


@Client.on_callback_query(filters.regex(r"^add"))
@authorized_users_only
async def add_handler_query(client: Client, query: CallbackQuery) -> None:
    query_data = query.data.split()[1]
    chat_id, user_id = query.message.chat.id, query.from_user.id

    data = "user_id" if query_data == "admin" else "chat_id"
    entity = "admin" if query_data == "admin" else "fsub"
    await query.message.edit_text(
        f"Send a new {data} to add {entity}",
        reply_markup=ikb(helper_buttons.Cancel),
    )

    new_id = None
    buttons = (
        ikb(helper_buttons.Admins_)
        if query_data == "admin"
        else ikb(helper_buttons.FSubs_)
    )
    try:
        listening = await client.listen(chat_id=chat_id, user_id=user_id)
        await listening.delete()
        new_id = int(listening.text)
    except errors.ListenerStopped:
        await query.message.edit_text(
            "Process has been cancelled!", reply_markup=buttons
        )
        return
    except Exception:
        await query.message.edit_text(
            f"Invalid! Just send a {data}", reply_markup=buttons
        )
        return

    list_ids = await get_admins() if query_data == "admin" else await get_fs_chats()
    if new_id in list_ids:
        await query.message.edit_text(
            f"Thats {data} already added", reply_markup=buttons
        )
        return

    try:
        chat = await client.get_chat(new_id)
        if query_data == "admin" and chat.type != ChatType.PRIVATE:
            raise Exception
        elif query_data == "fsub" and chat.type not in [
            ChatType.SUPERGROUP,
            ChatType.CHANNEL,
        ]:
            raise Exception
    except Exception:
        await query.message.edit_text(
            f"Thats {data} isn't valid!", reply_markup=buttons
        )
        return

    if query_data == "admin":
        await add_admin(new_id)
        await helper_handlers.admins_init()
    elif query_data == "fsub":
        await add_fs_chat(new_id)
        await helper_handlers.fs_chats_init()

    await query.message.edit_text(
        f"Added new {entity}: <code>{new_id}</code>", reply_markup=buttons
    )


@Client.on_callback_query(filters.regex(r"^del"))
@authorized_users_only
async def del_handler_query(client: Client, query: CallbackQuery) -> None:
    query_data = query.data.split()[1]
    chat_id, user_id = query.message.chat.id, query.from_user.id

    data = "user_id" if query_data == "admin" else "chat_id"
    entity = "admin" if query_data == "admin" else "fsub"
    await query.message.edit_text(
        f"Send a new {data} to delete {entity}",
        reply_markup=ikb(helper_buttons.Cancel),
    )

    get_id = None
    buttons = (
        ikb(helper_buttons.Admins_)
        if query_data == "admin"
        else ikb(helper_buttons.FSubs_)
    )
    try:
        listening = await client.listen(chat_id=chat_id, user_id=user_id)
        await listening.delete()
        get_id = int(listening.text)
    except errors.ListenerStopped:
        await query.message.edit_text(
            "Process has been cancelled!", reply_markup=buttons
        )
        return
    except Exception:
        await query.message.edit_text(
            f"Invalid! Just send a {data}", reply_markup=buttons
        )
        return

    list_ids = await get_admins() if query_data == "admin" else await get_fs_chats()
    if get_id not in list_ids:
        await query.message.edit_text(f"Thats {data} not found", reply_markup=buttons)
        return

    if query_data == "admin":
        await del_admin(get_id)

        logger.info("Bot Admins: Initializing...")
        await helper_handlers.admins_init()

    elif query_data == "fsub":
        await del_fs_chat(get_id)

        logger.info("Sub. Chats: Initializing...")
        await helper_handlers.fs_chats_init()

    await query.message.edit_text(
        f"The {entity} has been deleted: <code>{get_id}</code>",
        reply_markup=buttons,
    )
