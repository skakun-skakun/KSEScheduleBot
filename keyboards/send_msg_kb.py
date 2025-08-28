from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

send_msg_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text="Хочу щоб бот працював!", callback_data="bot_please_work"
)]])
