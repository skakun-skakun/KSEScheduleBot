import os

from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import parser

router = Router()


@router.message(StateFilter(None), Command('update_dfs'), F.from_user.id == int(os.getenv("ADMIN_ID")))
async def update_dfs(message: Message, state: FSMContext):
    parser.update_dfs()
    await message.answer("Parser updated")
    await state.clear()
