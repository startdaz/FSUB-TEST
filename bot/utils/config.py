import os


class Config:
    API_ID = int(os.environ.get("API_ID", 1234))
    API_HASH: str = os.environ.get("API_HASH", "b184")
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "7u9jl")
    OWNER_ID = int(os.environ.get("OWNER_ID", 4879))
    MONGODB_URI: str = os.environ.get("MONGODB_URI", "mongodb://root:passwd@mongo")
    DATABASE_CHAT_ID = int(os.environ.get("DATABASE_CHAT_ID" -100))


config: "Config" = Config()
BOT_ID = config.BOT_TOKEN.split(":", 1)[0]
