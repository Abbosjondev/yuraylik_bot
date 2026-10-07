import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlalchemy import select

from core.config import BOT_TOKEN
from db.database import AsyncSessionLocal
from db.models import User
from db.bitmaps import user_records, offer_accepted_users
from middlewares.database import DatabaseMiddleware
from middlewares.new_user import DatabaseUpsertMiddleware
from handlers.start import router as start_router
from handlers.chat_member import router as chat_member_router
from handlers.activity import router as activity_router

dp = Dispatcher()
dp.update.middleware(DatabaseMiddleware())
dp.message.middleware(DatabaseUpsertMiddleware())
dp.include_routers(start_router, chat_member_router, activity_router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def onstartup():
    logger.info("Kesh ma'lumotlar bazasidan yuklanmoqda...")
    async with AsyncSessionLocal() as session:

        result = await session.execute(select(User.telegram_id, User.is_offer_accepted))
        rows = result.all()

        all_users = [tid for tid, _ in rows]
        offer_accepted_ids = [tid for tid, accepted in rows if accepted]

        user_records.update(all_users)
        offer_accepted_users.update(offer_accepted_ids)
    logger.info(f"Kesh muvaffaqiyatli tiklandi! {len(user_records)=} va {len(offer_accepted_users)=}")

async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found!")
    bot = Bot(BOT_TOKEN)

    dp.startup.register(onstartup)

    await dp.start_polling(bot)

try:
    if __name__ == "__main__":
        asyncio.run(main())
except KeyboardInterrupt:
    pass