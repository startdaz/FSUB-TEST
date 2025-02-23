import os
from dotenv import load_dotenv

# Muat variabel dari file .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Ambil path FSUB-TEST
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH, override=True)  # Pastikan variabel di .env digunakan

class Config:
    API_ID = int(os.getenv("API_ID")) if os.getenv("API_ID") else None
    API_HASH = os.getenv("API_HASH") or ""
    BOT_TOKEN = os.getenv("BOT_TOKEN") or ""
    OWNER_ID = int(os.getenv("OWNER_ID")) if os.getenv("OWNER_ID") else None
    MONGODB_URI = os.getenv("MONGODB_URI") or ""
    DATABASE_CHAT_ID = int(os.getenv("DATABASE_CHAT_ID")) if os.getenv("DATABASE_CHAT_ID") else None

config = Config()
BOT_ID = config.BOT_TOKEN.split(":", 1)[0] if config.BOT_TOKEN else None


"""
import os


class Config:
    API_ID = int(os.environ.get("API_ID", 1234)) #GANTI "1234" DENGAN API_ID
    API_HASH: str = os.environ.get("API_HASH", "b184") #GANTI "b184" DENGAN API_HASH , JANGAN HAPUS TANDA (" ") NYA !!!
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "7u9jl") #GANTI "7u9jl" DENGAN TOKEN BOT , JANGAN HAPUS TANDA (" ") NYA !!!
    OWNER_ID = int(os.environ.get("OWNER_ID", 1234)) #GANTI "1234" DENGAN ID PEMILIK BOT
    MONGODB_URI: str = os.environ.get("MONGODB_URI", "mongodb://root:passwd@mongo") #GANTI "mongodb://root:passwd@mongo" DENGAN URI MONGO , JANGAN HAPUS TANDA (" ") NYA !!!
    DATABASE_CHAT_ID = int(os.environ.get("DATABASE_CHAT_ID", -100)) #GANTI DENGAN DATABASE CHANNEL


config: "Config" = Config()
BOT_ID = config.BOT_TOKEN.split(":", 1)[0]
"""
