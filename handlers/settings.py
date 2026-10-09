from datetime import datetime, time

from aiogram import F, Router
from aiogram.types import CallbackQuery, ForceReply, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from handlers.fsm import NotificationTime
from handlers.functions import send_or_edit_settings_message, show_home_menu
from keyboards.reply import back_keyboard


router = Router()


@router.message(F.text == "⚙️ Sozlamalar")
async def add_record_wait(message: Message, session: AsyncSession):
    if not message.from_user:
        return
    user = await session.get(User, message.from_user.id)
    if not user:
        return
    await send_or_edit_settings_message(message, user)


@router.callback_query(F.data == "rating_visible")
async def change_rating_visible_status(callback: CallbackQuery, session: AsyncSession):
    if not callback.from_user or not isinstance(callback.message, Message):
        await callback.answer("Bu xabar juda eski", show_alert=True)
        return

    if not callback.from_user:
        return
    user = await session.get(User, callback.from_user.id)
    if not user:
        return
    user.is_visible = not user.is_visible
    await send_or_edit_settings_message(callback, user, True)
    await session.commit()


@router.callback_query(F.data == "daily_notification")
async def change_notification_time(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    if not callback.from_user or not isinstance(callback.message, Message):
        await callback.answer("Bu xabar juda eski", show_alert=True)
        return

    if not callback.from_user:
        return
    user = await session.get(User, callback.from_user.id)
    if not user:
        return

    if bool(user.notification_time):
        user.notification_time = None
        await send_or_edit_settings_message(callback, user, True)
    else:
        await callback.message.delete()
        await callback.message.answer(
            "Eslatma qaysi vaqtda xabar yuborilishini xohlaysiz?\n\nAniq vaqtni kiriting (masalan: 07:00 yoki 20:30)",
            reply_markup=back_keyboard(
                input_field_placeholder="Vaqtni kiriting (08:00) formatda"
            ),
        )
        await state.set_state(NotificationTime.wait_for_time)
    await session.commit()


@router.message(NotificationTime.wait_for_time)
async def set_notification_time(
    message: Message, session: AsyncSession, state: FSMContext
):
    text = message.text or ""
    if text == "🔙 Orqaga":
        await show_home_menu(message)
        await state.clear()
        return

    if not message.text or not message.from_user:
        return
    user_message = message.text.strip()
    try:
        parsed = time.fromisoformat(user_message)
        user = await session.get(User, message.from_user.id)
        if not user:
            return
        user.notification_time = parsed.strftime("%H:%M")

        await message.answer("O'rnatildi ✅")
        await show_home_menu(message)
        await send_or_edit_settings_message(message, user)

        await state.clear()
        await session.commit()
    except ValueError:
        await message.answer(
            "Vaqtni to'g'ri formatda kiriting\n\nmasalan: 07:00 yoki 20:30"
        )
