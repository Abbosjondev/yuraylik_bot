import asyncio
import logging

from aiogram import Bot, Dispatcher

from core.config import BOT_TOKEN
from middlewares.database import DatabaseMiddleware
from middlewares.new_user import DatabaseUpsertMiddleware
from handlers.start import router as start_router
from handlers.chat_member import router as chat_member_router

dp = Dispatcher()
dp.update.middleware(DatabaseMiddleware())
dp.message.middleware(DatabaseUpsertMiddleware())
dp.include_routers(start_router, chat_member_router)


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found!")
    bot = Bot(BOT_TOKEN)

    await dp.start_polling(bot)

try:
    if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        asyncio.run(main())
except KeyboardInterrupt:
    pass