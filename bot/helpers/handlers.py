from typing import Dict, List

from pyrogram import enums, errors

from ..base import bot
from ..db_funcs import get_admins, get_fs_chats
from ..utils import config, logger
from .url_safe import url_safe


class HelperHandlers:
    def __init__(self, client) -> None:
        self.client = client
        self.admins: [List[int]] = []
        self.fs_chats: Dict[int, Dict[str, str]] = {}

    async def admins_init(self) -> [List[int]]:
        self.admins = []

        admin_ids = await get_admins()
        if admin_ids:
            self.admins = admin_ids + [config.OWNER_ID]
        else:
            self.admins = [config.OWNER_ID]

        for i, user_id in enumerate(self.admins):
            logger.info(f"Bot Admin {i + 1} = {user_id}")

        return self.admins

    async def fs_chats_init(self) -> Dict[int, Dict[str, str]]:
        self.fs_chats.clear()

        fs_chats = await get_fs_chats()
        if fs_chats:
            for i, chat_id in enumerate(fs_chats):
                try:
                    i = i + 1
                    chat = await self.client.get_chat(chat_id=chat_id)
                    chat_type = (
                        "Group"
                        if chat.type
                        in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]
                        else "Channel"
                    )
                    invite_link = chat.invite_link
                    self.fs_chats[chat_id] = {
                        "chat_type": chat_type,
                        "invite_link": invite_link,
                    }
                    logger.info(f"Sub. Chat {i} = {chat_id}")
                except errors.RPCError as e:
                    logger.warning(f"Sub. Chat {i} = {chat_id}", exc_info=e)
        else:
            logger.info("Sub. Chats = None")

        return self.fs_chats

    async def user_is_not_join(self, user_id) -> List[int]:
        chat_ids = [key for key in self.fs_chats.keys()]
        if not chat_ids or user_id in self.admins:
            return None

        already_join = set()
        for chat_id in chat_ids:
            try:
                await self.client.get_chat_member(chat_id, user_id)
                already_join.add(chat_id)
            except errors.RPCError:
                continue

        return [_ids for _ids in chat_ids if _ids not in already_join]

    def decode_data(self, encoded_data: str) -> List[int]:
        database_chat_id = config.DATABASE_CHAT_ID
        decoded_data = url_safe.decode_data(encoded_data).split("-")
        if len(decoded_data) == 2:
            return [int(int(decoded_data[1]) / abs(database_chat_id))]
        elif len(decoded_data) == 3:
            start_id = int(int(decoded_data[1]) / abs(database_chat_id))
            end_id = int(int(decoded_data[2]) / abs(database_chat_id))
            if start_id < end_id:
                return range(start_id, end_id + 1)
            else:
                return range(start_id, end_id - 1, -1)


helper_handlers: HelperHandlers = HelperHandlers(bot)
