from aiogram import Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User

router = Router()

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, session: AsyncSession):
    telegram_id = event.from_user.id
    await session.execute(update(User).where(User.telegram_id == telegram_id).values(is_active=False))
    await session.commit()

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, session: AsyncSession):
    telegram_id = event.from_user.id
    await session.execute(update(User).where(User.telegram_id == telegram_id).values(is_active=True))
    await session.commit()