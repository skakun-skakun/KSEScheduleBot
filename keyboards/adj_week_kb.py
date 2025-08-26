from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def adj_week_kb(email_or_name, week: int):
    if week == 1:
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🚫", callback_data="empty_one"),
            InlineKeyboardButton(text=f"Next week ({week+1}) >>", callback_data=f"week_schedule`{email_or_name}`{week+1}"),
        ]])
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=f"<< Prev week ({week-1})", callback_data=f"week_schedule`{email_or_name}`{week-1}"),
        InlineKeyboardButton(text=f"Next week ({week+1}) >>", callback_data=f"week_schedule`{email_or_name}`{week+1}"),
    ]])
