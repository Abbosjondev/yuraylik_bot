from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud import add_or_update_activity, update_user_streak
from handlers.functions import show_home_menu
from keyboards.reply import back_keyboard
from .fsm import AddRecordFSM


router = Router()

@router.message(F.text == '➕ Kiritish')
async def add_record_wait(message: Message, state: FSMContext):
    reply_keyboard = back_keyboard(input_field_placeholder="Daqiqa kiriting, masalan 15", one_time_keyboard=True)
    await message.answer('🚶‍♂️ Bugun qancha yurdingiz? (Daqiqalarda)\n\nSonlarda kiriting:', reply_markup=reply_keyboard)
    await state.set_state(AddRecordFSM.wait_for_minutes)

@router.message(AddRecordFSM.wait_for_minutes)
async def add_record_or_back(message: Message, state: FSMContext, session: AsyncSession):
    reply_keyboard = back_keyboard(input_field_placeholder="Daqiqa kiriting, masalan 15", one_time_keyboard=True)

    text = message.text or ""
    if text == '🔙 Orqaga':
        await show_home_menu(message)
        await state.clear()
        return

    if not text.isdigit():
        await message.answer("So'z yoki harf emas. Faqat raqam kiriting, masalan: 15", reply_markup=reply_keyboard)
        return

    number = int(text)

    if number <= 0 or number >= 600:
        await message.answer("Xato raqam. Siz juda katta yoki kichik raqam kiritdingiz. Iltimos to'g'ri raqamni kiriting.", reply_markup=reply_keyboard)
        return

    if message.from_user is None:
        await message.answer('Xatolik yuz berdi. Qayta urinib ko\'ring')
        return
    
    user_record = await add_or_update_activity(session, message.from_user.id, number)
    
    total = user_record["duration_minutes"]
    if user_record["is_updated"]:
        body = (
            f"✅ Saqlandi\n\n"
            f"Bugun hisobida jami {total} daqiqa yurdingiz.\n\n"
            f"Shunday davom eting."
        )
    else:
        body = "✅ Saqlandi\n\nShunday davom eting."
    await message.answer(body, reply_markup=ReplyKeyboardRemove())
    await show_home_menu(message)
    await state.clear()
    await update_user_streak(session, message.from_user.id, number)