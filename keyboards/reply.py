from aiogram.utils.keyboard import ReplyKeyboardBuilder

def home_menu_keyboards():
    builder = ReplyKeyboardBuilder()
    builder.button(text="➕ Kiritish")
    builder.button(text="⚡️ Statistika")
    builder.button(text="🏆 Reyting")
    builder.button(text="⚙️ Sozlamalar")
    builder.adjust(1, 1, 2)

    return builder.as_markup(resize_keyboard=True)

def back_keyboard(*, input_field_placeholder=None, one_time_keyboard=False):
    builder = ReplyKeyboardBuilder()
    builder.button(text='🔙 Orqaga')

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder=input_field_placeholder,
        one_time_keyboard=one_time_keyboard,
    )