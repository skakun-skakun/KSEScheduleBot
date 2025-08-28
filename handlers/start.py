from aiogram import types, Router, F
from keyboards.send_msg_kb import send_msg_kb
from bot import bot
import os
from aiogram.types import LinkPreviewOptions

# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart, Command
# from aiogram.fsm.context import FSMContext

router = Router()


@router.message()
async def on_any_message(message: types.Message):
    await message.answer("На жаль, бота було зупинено, бо шішка успішно догенерувала сайт розкладу: https://schedule.kse.ua/\nОднак якщо хочете щоб бот далі працював, тицьніть на кнопку нижче", reply_markup=send_msg_kb, link_preview_options=LinkPreviewOptions(is_disabled=True))


@router.callback_query(F.data == 'bot_please_work')
async def bot_work(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    await bot.send_message(os.getenv("LOGS_CHAT_ID"), f"{call.from_user.username if call.from_user.username else call.from_user.first_name + ' ' + call.from_user.last_name} ({call.from_user.id}) wants bot to work")
    await call.message.edit_text("Повідомлення відправлено ✅")

# @router.message(CommandStart())
# async def start(message: types.Message):
#     await message.answer('<b>Hello, world!</b>\nTo get yourself a schedule, use one of the given commands\n/week_schedule\n/interval_schedule', parse_mode=ParseMode.HTML)
#
#
# @router.message(Command("help"))
# async def cancel_state(message: types.Message, state: FSMContext):
#     await message.answer('Available Commands:\n/help – Show this help message\n/week_schedule – Get a schedule for a specific week number\n/interval_schedule – Get a schedule for a custom date range\n/cancel – Cancel the current action and start over')
#     await state.clear()
#
#
# @router.message(Command("cancel"))
# async def cancel_state(message: types.Message, state: FSMContext):
#     await message.answer('Canceled current action')
#     await state.clear()

