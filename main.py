import os
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

import asyncio

from aiogram import Bot, Dispatcher
from sqlalchemy import select

from core.config import BOT_TOKEN, WEBHOOK_URL, logger
from db.database import AsyncSessionLocal
from db.models import User
from db.bitmaps import user_records, offer_accepted_users
from middlewares.database import DatabaseMiddleware
from middlewares.new_user import DatabaseUpsertMiddleware
from handlers.start import router as start_router
from handlers.chat_member import router as chat_member_router
from handlers.activity import router as activity_router
from handlers.statistics import router as statistics_router
from handlers.settings import router as settings_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.notification_service import check_and_send_notification

dp = Dispatcher()
dp.update.middleware(DatabaseMiddleware())
dp.message.middleware(DatabaseUpsertMiddleware())
dp.include_routers(start_router, chat_member_router, activity_router, statistics_router, settings_router)

scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")

async def onstartup(bot: Bot):
    logger.info("Kesh ma'lumotlar bazasidan yuklanmoqda...")
    async with AsyncSessionLocal() as session:

        result = await session.execute(select(User.telegram_id, User.is_offer_accepted))
        rows = result.all()

        all_users = [tid for tid, _ in rows]
        offer_accepted_ids = [tid for tid, accepted in rows if accepted]

        user_records.update(all_users)
        offer_accepted_users.update(offer_accepted_ids)
    logger.info(f"Kesh muvaffaqiyatli tiklandi! {len(user_records)=} va {len(offer_accepted_users)=}")

    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    logger.info("Bot webhook ishga tushdi!")

    scheduler.add_job(
        check_and_send_notification,
        trigger="cron",
        minute='*',
        second='0',
        kwargs={"bot": bot},
        max_instances=1,
        coalesce=True
    )

    scheduler.start()

async def on_bot_shutdown(bot: Bot):
    await bot.delete_webhook()
    logger.info("Bot to'xtatildi!")

dp.startup.register(onstartup)
dp.shutdown.register(on_bot_shutdown)

async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found!")
    bot = Bot(BOT_TOKEN)

    app = web.Application()

    webhook_request_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )

    webhook_request_handler.register(app, path='/webhook')

    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=8000)

try:
    if __name__ == "__main__":
        asyncio.run(main())
except KeyboardInterrupt:
    pass