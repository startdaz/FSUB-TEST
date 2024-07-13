import os


class Config:
    API_ID = int(os.environ.get("API_ID", 2040))
    API_HASH: str = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
    OWNER_ID = int(os.environ.get("OWNER_ID", 487936750))
    MONGODB_URI: str = os.environ.get("MONGODB_URI", "mongodb://root:passwd@mongo")
    DATABASE_CHAT_ID = int(os.environ.get("DATABASE_CHAT_ID"))


config: "Config" = Config()
BOT_ID = config.BOT_TOKEN.split(":", 1)[0]
