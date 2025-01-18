import asyncio
import shlex
import sys

from meval import meval
from pyrogram import Client, filters
from pyrogram.helpers import ikb
from pyrogram.types import CallbackQuery, Message

from bot import add_restart_data_id, config, helper_buttons, write_doc

reply_markup = ikb(helper_buttons.Eval)


@Client.on_message(filters.user(config.OWNER_ID) & filters.command(["eval", "e"]))
async def evaluate_handler(client: Client, message: Message) -> None:
    if len(message.command) == 1:
        await message.reply_text(
            "<i>ʙᴇʀɪᴋᴀɴ ᴋᴏᴅᴇ ᴜɴᴛᴜᴋ ᴅɪᴇᴋꜱᴇᴋᴜꜱɪ</i>", quote=True, reply_markup=reply_markup
        )
        return

    reply_msg = await message.reply_text("...", quote=True)
    await async_evaluate_func(client, message, reply_msg)


@Client.on_callback_query(filters.regex(r"^eval$"))
async def evaluate_handler_query(client: Client, query: CallbackQuery) -> None:
    user_id = query.from_user.id
    author_id = query.message.reply_to_message.from_user.id
    if user_id != author_id:
        await query.answer("ʙᴜᴋᴀɴ ᴍɪʟɪᴋᴍᴜ!", show_alert=True)
        return

    chat_id, msg = query.message.chat.id, query.message
    message = await client.get_messages(chat_id, msg.reply_to_message.id)
    reply_msg = await client.get_messages(chat_id, msg.id)

    await async_evaluate_func(client, message, reply_msg)


@Client.on_message(filters.user(config.OWNER_ID) & filters.command(["shell", "sh"]))
async def shell_handler(client: Client, message: Message) -> None:
    if len(message.command) == 1:
        await message.reply_text("<i>ʙᴇʀɪᴋᴀɴ ᴋᴏᴅᴇ ʙᴀꜱʜ ᴜɴᴛᴜᴋ ᴅɪᴇᴋꜱᴇᴋᴜꜱɪ!</i>", quote=True)
        return

    shell_code = message.text.split(maxsplit=1)[1]
    shell_args = shlex.split(shell_code)

    exec_msg = await message.reply_text("<i>ᴍᴇɴᴊᴀʟᴀɴᴋᴀɴ ᴋᴏᴅᴇ ʙᴀꜱʜ...</i>", quote=True)

    shell_result = ""
    try:
        exec_bash = await asyncio.create_subprocess_exec(
            *shell_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await exec_bash.communicate()
        shell_result = (stdout + stderr).decode().strip()
    except Exception as e:
        shell_result = e

    final_output = f"<blockquote expandable><code>{shell_result}</code></blockquote>"
    if len(final_output) > 4096:
        await write_doc("shell_output.txt", shell_result)

        await exec_msg.edit_text("<i>ᴏᴜᴛᴘᴜᴛ ᴛᴇʀʟᴀʟᴜ ʙᴇꜱᴀʀ, ᴋɪʀɪᴍᴋᴀɴ ꜱᴇʙᴀɢᴀɪ ᴅᴏᴄ...</i>")
        await client.send_document(
            message.chat.id,
            "shell_output.txt",
            reply_to_message_id=exec_msg.id,
        )

        return

    await exec_msg.edit_text(final_output)


@Client.on_message(filters.user(config.OWNER_ID) & filters.command(["logs", "log"]))
async def logs_handler(_, message: Message) -> None:
    await message.reply_document("logs.txt", quote=True)


@Client.on_message(filters.user(config.OWNER_ID) & filters.command(["restart", "r"]))
async def restart_handler(client: Client, message: Message) -> None:
    self_msg = await message.reply_text("<i>ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ...</i>", quote=True)

    chat_id, message_id = message.chat.id, self_msg.id
    await add_restart_data_id(chat_id, message_id)

    await asyncio.create_subprocess_exec(sys.executable, *sys.argv)


async def async_evaluate_func(
    client: Client, message: Message, reply_msg: Message
) -> None:
    await reply_msg.edit_text("<i>ᴍᴇɴᴊᴀʟᴀɴᴋᴀɴ ᴋᴏᴅᴇ...</i>")

    if len(message.text.split()) == 1:
        await reply_msg.edit("<i>ᴋᴏᴅᴇ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ!</i>", reply_markup=reply_markup)
        return

    eval_vars = {
        "c": client,
        "m": message,
        "r": message.reply_to_message,
        "u": (message.reply_to_message or message).from_user,
    }

    eval_result = ""
    eval_code = message.text.split(maxsplit=1)[1]
    try:
        eval_result = await meval(eval_code, globals(), **eval_vars)
    except Exception as e:
        eval_result = e

    result_output = f"<blockquote expandable><code>{eval_result}</code></blockquote>"
    if len(result_output) > 4096:
        await write_doc("eval_output.txt", str(eval_result))

        await reply_msg.edit_text(
            "<i>ᴏᴜᴛᴘᴜᴛ ᴛᴇʀʟᴀʟᴜ ʙᴇꜱᴀʀ, ᴋɪʀɪᴍᴋᴀɴ ꜱᴇʙᴀɢᴀɪ ᴅᴏᴄ...</i>",
            reply_markup=reply_markup,
        )
        await client.send_document(
            message.chat.id,
            "eval_output.txt",
            reply_to_message_id=reply_msg.id,
        )
        return

    await reply_msg.edit_text(result_output, reply_markup=reply_markup)
