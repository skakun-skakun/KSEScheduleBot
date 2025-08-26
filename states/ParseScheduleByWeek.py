from aiogram.fsm.state import StatesGroup, State


class ParseScheduleByWeek(StatesGroup):
    chosen_email = State()
    choosen_week = State()
