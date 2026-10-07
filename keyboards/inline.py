from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def offer_inline_button():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text="🌐 Maqolani ochish", 
        url="https://yuraylik.vercel.app"
    ))

    builder.add(InlineKeyboardButton(
        text="✅ Davom etamiz", 
        callback_data="offer_accepted"
    ))
    builder.adjust(1)
    return builder.as_markup()

