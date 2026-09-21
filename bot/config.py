import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

UPLOAD_CHAT_ID = int(os.getenv("UPLOAD_CHAT_ID", "0"))

ENABLE_COMPRESSION = os.getenv("ENABLE_COMPRESSION", "true").lower() == "true"
COMPRESS_HEIGHT = int(os.getenv("COMPRESS_HEIGHT", "480"))
COMPRESS_CRF = int(os.getenv("COMPRESS_CRF", "28"))

PORT = int(os.getenv("PORT", "8080"))
MAX_QUEUE = int(os.getenv("MAX_QUEUE", "10"))
MAX_FILE_GB = float(os.getenv("MAX_FILE_GB", "2"))

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "/tmp/skr_downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
