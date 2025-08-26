from aiogram.fsm.state import StatesGroup, State


class ParseScheduleByWeek(StatesGroup):
    chosen_email_or_name = State()
    choosen_week = State()
