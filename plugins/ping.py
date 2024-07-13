import datetime

from pyrogram import Client, filters
from pyrogram.helpers import ikb
from pyrogram.raw import functions
from pyrogram.types import CallbackQuery, Message

from bot import helper_buttons


@Client.on_message(filters.private & filters.command(["ping", "p"]))
async def ping_handler(client: Client, message: Message) -> None:
    latency = await ping_function(client)
    await message.reply_text(
        f"<b>Latency:</b> {latency}",
        quote=True,
        reply_markup=ikb(helper_buttons.Ping),
    )


@Client.on_callback_query(filters.regex(r"^ping$"))
async def ping_handler_query(client: Client, query: CallbackQuery) -> None:
    await query.message.edit_text("<i>Refreshing...</i>")
    latency = await ping_function(client)
    await query.message.edit_text(
        f"<b>Latency:</b> {latency}", reply_markup=ikb(helper_buttons.Ping)
    )


async def ping_function(client: Client) -> str:
    start_time = datetime.datetime.now()
    await client.invoke(functions.Ping(ping_id=0))
    end_time = datetime.datetime.now()

    return f"{(end_time - start_time).microseconds / 1000} ms"
