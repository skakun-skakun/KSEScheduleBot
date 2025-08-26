from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer('<b>Hello, world!</b>\nTo get yourself a schedule, use one of the given commands\n/week_schedule\n/interval_schedule', parse_mode=ParseMode.HTML)


@router.message(Command("cancel"))
async def cancel_state(message: types.Message, state: FSMContext):
    await message.answer('Canceled current action')
    await state.clear()

