from aiogram.fsm.state import StatesGroup, State


class ParseScheduleByInterval(StatesGroup):
    chosen_email = State()
    chosen_start_date = State()
    chosen_end_date = State()
