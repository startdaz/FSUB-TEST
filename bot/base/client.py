import sys
from typing import Any, Dict

from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, errors
from pyrogram.enums import ParseMode
from pyrogram.types import BotCommand

from ..utils import BOT_ID, config, logger

session_db = AsyncIOMotorClient(config.MONGODB_URI)


class Bot(Client):
    def __init__(self) -> None:
        name: str = f"{BOT_ID}_SESSION"
        api_id: int = config.API_ID
        api_hash: str = config.API_HASH
        bot_token: str = config.BOT_TOKEN
        bot_plugins: Dict[str, str] = {"root": "plugins"}
        bot_session_db: Dict[str, Any] = {"connection": session_db}

        super().__init__(
            name=name,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            plugins=bot_plugins,
            mongodb=bot_session_db,
        )

    async def start(self) -> None:
        try:
            await super().start()
            logger.info("Bot: Started")
        except errors.RPCError as e:
            logger.error(f"Bot: {e}", exc_info=False)
            sys.exit(1)

        logger.info("Bot: Commands...")
        await self.set_bot_commands(
            commands=[
                BotCommand("start", "Start the bot"),
                BotCommand("ping", "Latency of bot"),
            ]
        )
        logger.info('Bot: Commands = ["start", "ping"]')

        logger.info("Bot: ParseMode...")
        self.set_parse_mode(ParseMode.HTML)
        logger.info("Bot: ParseMode = HTML")

    async def stop(self) -> None:
        logger.info("Bot: Stopping...")
        await super().stop()


bot: Bot = Bot()
