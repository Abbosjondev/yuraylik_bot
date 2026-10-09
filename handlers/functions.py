from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message

from db.models import User
from keyboards.inline import offer_inline_button, settings_menu_buttons
from keyboards.reply import home_menu_keyboards


async def send_offer(message: Message):
    content = (
        "Boshlashdan oldin bu maqolani bir o'qib chiqing, tushib oling.\n\n"
        "O'qib-tushunib bo'lgach <b>«✅ Davom etamiz»</b> tugmasini bosing.\n\n"
        "https://yuraylik.vercel.app"
    )
    await message.answer(content, parse_mode="HTML", reply_markup=offer_inline_button())


async def show_home_menu(message: Message):
    await message.answer("🏠 Asosiy menyudasiz", reply_markup=home_menu_keyboards())


async def send_or_edit_settings_message(
    event: Message | CallbackQuery, user: User, edit: bool = False
):
    if isinstance(event, CallbackQuery):
        target_message = event.message if isinstance(event.message, Message) else None
    else:
        target_message = event

    if not isinstance(target_message, Message):
        return

    reply_markup = settings_menu_buttons(bool(user.notification_time), user.is_visible)
    if edit:
        try:
            await target_message.edit_reply_markup(reply_markup=reply_markup)
        except TelegramBadRequest:
            pass
    else:
        await target_message.answer(
            "Sozlamalar menyusi: 👇\n\nBot har kuni eslatma yuborishini sozlash (o'chirish/yoqish)\nyoki sizni reytingdan o'chirish (yoki yoqish)ni sozlashingiz mumkin",
            reply_markup=reply_markup,
        )