from ..base import database
from ..utils import BOT_ID, logger


async def initial_database():
    default_start_text = (
        "ʜᴀʟʟᴏ, {mention}!\n"
        "ʙᴏᴛ ꜱᴜᴅᴀʜ ᴀᴋᴛɪꜰ ᴅᴀɴ ʙᴇʀᴊᴀʟᴀɴ. ʙᴏᴛ ɪɴɪ ᴅᴀᴘᴀᴛ ᴍᴇɴʏɪᴍᴘᴀɴ ᴘᴇꜱᴀɴ ᴅᴀʟᴀᴍ ᴏʙʀᴏʟᴀɴ ᴋʜᴜꜱᴜꜱ, "
        "ᴅᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴍᴇɴɢᴀᴋꜱᴇꜱɴʏᴀ ᴍᴇʟᴀʟᴜɪ ʙᴏᴛ.\n"
        " \n"
        "ʙᴏᴛ ɪɴɪ ᴅɪᴋᴇʟᴏʟᴀ ᴏʟᴇʜ [ᴇᴍɪɴ](https://t.me/{})\n".format(me.username , 'iniemin')
    )
    default_force_text = (
        "ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴘᴇꜱᴀɴ ʏᴀɴɢ ᴅɪʙᴀɢɪᴋᴀɴ ᴏʟᴇʜ ʙᴏᴛ. ʙᴇʀɢᴀʙᴜɴɢʟᴀʜ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ, ʟᴀʟᴜ ᴛᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ ᴄᴏʙᴀ ʟᴀɢɪ."
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
