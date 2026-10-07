from aiogram.types import Message

from keyboards.inline import offer_inline_button
from keyboards.reply import home_menu_keyboards


async def send_offer(message: Message):
    content = ("Boshlashdan oldin bu maqolani bir o'qib chiqing, tushib oling.\n\n"
               "O'qib-tushunib bo'lgach <b>«✅ Davom etamiz»</b> tugmasini bosing.\n\n"
               "https://yuraylik.vercel.app")
    await message.answer(content, parse_mode="HTML", reply_markup=offer_inline_button())

async def show_home_menu(message: Message):
    await message.answer("🏠 Asosiy menyudasiz", reply_markup=home_menu_keyboards())