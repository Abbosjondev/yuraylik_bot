import html

from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy import and_, func, or_, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from db.bitmaps import rating_cache

from db.models import User


router = Router()


@router.message(F.text == "⚡️ Statistika")
async def statistics_menu(message: Message, session: AsyncSession):
    if message.from_user is None:
        return

    user_id = message.from_user.id

    user = await session.get(User, user_id)
    if user is None:
        return

    rank_stmt = select(func.count()).select_from(User).where(
        or_(
            User.current_streak > user.current_streak,
            and_(User.current_streak == user.current_streak, User.highest_streak > user.highest_streak),
            and_(
                User.current_streak == user.current_streak,
                User.highest_streak == user.highest_streak,
                User.total_minutes > user.total_minutes
            )
        )
    )

    higher_users_count = await session.scalar(rank_stmt)
    user_rank = (higher_users_count or 0) + 1

    streak_text = f"🔥 <b>Davomiylik:</b> {user.current_streak}"
    if user.highest_streak > user.current_streak:
        streak_text += f" <i>(eng yuqori: {user.highest_streak})</i>"

    context = (
        f"{streak_text}\n\n"
        f"Siz hozirgacha {user.total_minutes} daqiqa yurdingiz.\n\n"
        f"🏆 Barcha foydalanuvchilar orasida <b>{user_rank}</b>-o'rindasiz."
    )
    await message.answer(context, parse_mode="HTML")

@router.message(F.text == "🏆 Reyting")
async def rating_menu(message: Message, session: AsyncSession):
    if "top_20" in rating_cache:
        await message.answer(str(rating_cache["top_20"]), parse_mode="HTML")
        return

    stmt = select(User).order_by(
        User.current_streak.desc(),
        User.highest_streak.desc(),
        User.total_minutes.desc()
    ).limit(20)

    result = await session.scalars(stmt)
    top_users = result.all()

    if not top_users:
        await message.answer("Hozircha reyting bo'sh.")
        return

    lines = ["<b>🏆 TOP-20 foydalanuvchilar:</b>\n"]

    for index, u in enumerate(top_users, start=1):
        self_name = html.escape(u.full_name)
        lines.append(f"<b>{index}.</b> <a href=\"tg://user?id={u.telegram_id}\">{self_name}</a> - 🔥 {u.current_streak} / {u.total_minutes} daq")

    final_text = "\n".join(lines)
    rating_cache["top_20"] = final_text

    await message.answer(final_text, parse_mode="HTML")