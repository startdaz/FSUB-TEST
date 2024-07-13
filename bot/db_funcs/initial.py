from ..base import database
from ..utils import BOT_ID, logger


async def initial_database():
    default_start_text = (
        "Hello, {mention}!\n"
        "The bot is up and running. These bots can store messages in custom chats, "
        "and users access them through the bot."
    )
    default_force_text = (
        "To view messages shared by bots. Join first, then press the Try Again button."
    )

    default_key_value_db = {
        "GENERATE_URL": True,
        "PROTECT_CONTENT": True,
        "FORCE_TEXT": default_force_text,
        "START_TEXT": default_start_text,
    }

    data: str = ""
    for key, value in default_key_value_db.items():
        if key == "GENERATE_URL":
            data = "Generate Status"
        else:
            data = key.title().replace("_", " ")

        try:
            doc = await database.get_doc(int(BOT_ID))
            if doc is None or key not in doc:
                raise KeyError
            logger.info(f"{data} = Existed")
        except KeyError:
            await database.add_value(int(BOT_ID), key, value)
            logger.info(f"{data} = Default")
