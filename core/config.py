import logging
import os
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "false").lower() == "true"

TASHKENT_TZ = ZoneInfo("Asia/Tashkent")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)