import asyncio
from datetime import datetime
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiolimiter import AsyncLimiter
from sqlalchemy import select
from db.models import User
from core.config import TASHKENT_TZ, logger
from db.database import AsyncSessionLocal



rate_limiter = AsyncLimiter(max_rate=28, time_period=1.0)

async def send_reminder(bot: Bot, user_id: int, text: str):
    async with rate_limiter:
        try:
            await bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")
            return True
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            return await send_reminder(bot, user_id, text)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Notification send error: {user_id=} {e}")
            return False

async def check_and_send_notification(bot: Bot):
    now_time = datetime.now(TASHKENT_TZ).time().replace(second=0, microsecond=0).strftime("%H:%M")

    async with AsyncSessionLocal() as session:
        stmt = (
            select(User.telegram_id)
            .where(User.notification_time == now_time, User.is_active == True)
        )
        result = await session.scalars(stmt)

        batch = []
        text = "⏰ <b>Eslatma</b>\n\nSiz xohlayotgan vaqt keldi. Shu vaqtda eslatishimni belgilagan edingiz."

        for user_id in result:
            batch.append(send_reminder(bot, user_id, text))

            if len(batch) >=28:
                await asyncio.gather(*batch)
                batch.clear()
                await asyncio.sleep(0.05)
        if batch:
            await asyncio.gather(*batch)



