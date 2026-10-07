from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy import text, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.bitmaps import offer_accepted_users
from db.models import User
from handlers.functions import send_offer, show_home_menu

router = Router()

@router.callback_query(F.data == 'offer_accepted')
async def accept_offer_handler(callback: CallbackQuery, session: AsyncSession):
    if not isinstance(callback.message, Message):
        await callback.answer("Xabar eskirgan, iltimos /start bosing", show_alert=True)
        return
    
    await callback.message.delete()
    
    if callback.from_user.id not in offer_accepted_users:
        offer_accepted_users.add(callback.from_user.id)
        await callback.answer("Yaxshi. O'qib chiqqaningizdan xursandman 👍")
        await show_home_menu(callback.message)
        await session.execute(
            update(User)
            .where(User.telegram_id == callback.from_user.id)
            .values(is_offer_accepted=True)
        )
        await session.commit()
    else:
        await callback.answer()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    if not user: return

    if user.id in offer_accepted_users:
        await show_home_menu(message)
        return

    content = (f"<b>Assalomu alaykum <a href=\"tg://user?id={user.id}\">{user.full_name}</a>!</b>\n\n"
               "O'zingizni rivojlantirish, yurish odatini shakllantirishga qaror qilganingiz bilan tabriklayman\n\n"
               "Xush kelibsiz!")

    await message.answer(content, parse_mode="HTML")

    await send_offer(message)