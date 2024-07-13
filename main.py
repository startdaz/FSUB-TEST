import asyncio
import sys

from pyrogram import errors

from bot import (
    bot,
    config,
    database,
    del_restart_data_id,
    get_restart_data_ids,
    helper_handlers,
    initial_database,
    logger,
)


async def main() -> None:
    logger.info("MongoDB: Connecting...")
    await database.connect()

    logger.info("Bot: Starting...")
    await bot.start()

    async def chat_db_init() -> None:
        chat_id = config.DATABASE_CHAT_ID
        try:
            hello = await bot.send_message(chat_id, "Hello World!")
            await hello.delete()
            logger.info(f"Database Chat = {chat_id}")
        except errors.RPCError as e:
            logger.error(f"Database Chat = {chat_id}", exc_info=e)
            sys.exit(1)

    async def restart_data_init() -> None:
        try:
            restart_data = await get_restart_data_ids()
            cid, mid = restart_data.get("chat_id"), restart_data.get("message_id")
            await bot.send_message(
                cid, "<i>Bot has been restarted</i>", reply_to_message_id=mid
            )

            await del_restart_data_id()
            logger.info(f"RestartID: {cid} {mid}")

        except Exception:
            logger.info("RestartID: Not Found")

            return None

    async def cache_db_init() -> None:
        await asyncio.gather(
            helper_handlers.admins_init(),
            helper_handlers.fs_chats_init(),
        )

    logger.info("Database Chat: Initializing...")
    await chat_db_init()

    logger.info("MongoDB: Initializing...")
    await initial_database()

    logger.info("CacheDB: Initializing...")
    await cache_db_init()

    logger.info("RestartID: Finding...")
    await restart_data_init()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
        logger.info(f"Bot: ID = {bot.me.id}")
        logger.info(f"Bot: Username = @{bot.me.username}")
        logger.info("Bot: Activated!")
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt: Terminating...")
    except Exception as e:
        logger.error(e, exc_info=False)
    finally:
        loop.run_until_complete(bot.stop())
        logger.info("Bot: Stopped")
        loop.close()
