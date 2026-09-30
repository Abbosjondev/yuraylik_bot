from collections.abc import Awaitable, Callable
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from cachetools import TTLCache

from db.crud import add_or_update_user

user_cache = TTLCache(maxsize=1000, ttl=86400)

class DatabaseUpsertMiddleware(BaseMiddleware):
    async def __call__(
            self, 
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], 
            event: TelegramObject, 
            data: dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            user = event.from_user
            if not user:
                return await handler(event, data)
            session: AsyncSession = data['session']
            if user.id not in user_cache:
                await add_or_update_user(session, user.id, user.full_name, user.username)
                user_cache[user.id] = True
        return await handler(event, data)