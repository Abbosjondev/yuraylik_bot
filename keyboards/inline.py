from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def offer_inline_button():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="🌐 Maqolani ochish", url="https://yuraylik.vercel.app"
        )
    )

    builder.add(
        InlineKeyboardButton(text="✅ Davom etamiz", callback_data="offer_accepted")
    )
    builder.adjust(1)
    return builder.as_markup()


def settings_menu_buttons(is_notification_on, is_rating_visible):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=("🔔" if is_notification_on else "🔕") + " Kundalik eslatma",
            callback_data="daily_notification",
            style=("success" if is_notification_on else "danger")
        )
    )

    builder.add(
        InlineKeyboardButton(
            text=("✅" if is_rating_visible else "🚫") + " Reytingda ko'rinish",
            callback_data="rating_visible",
            style=("success" if is_rating_visible else "danger")
        )
    )

    builder.adjust(1)

    return builder.as_markup()
