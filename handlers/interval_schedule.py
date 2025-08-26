from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot import parser
from states.ParseScheduleByInterval import ParseScheduleByInterval
from aiogram3_calendar import SimpleCalendar
from aiogram3_calendar.calendar_types import SimpleCalendarCallback

router = Router()


# @router.message(StateFilter(None), Command('calendar'))
# async def calendar(message: Message):
#     await message.answer('Pick a date', reply_markup=await SimpleCalendar().start_calendar())
#
#
# @router.callback_query(SimpleCalendarCallback.filter())
# async def process_selecion(call: CallbackQuery, callback_data: CallbackQuery):
#     selected, date = await SimpleCalendar().process_selection(call, callback_data)
#     if selected and date:
#         await call.message.edit_text(f"You selected: {date.isoformat()}")
#         await call.answer("")


@router.message(StateFilter(None), Command('interval_schedule'))
async def week_schedule_ask_email(message: Message, state: FSMContext):
    await message.answer("Enter email (without @kse.org.ua):")
    await state.set_state(ParseScheduleByInterval.chosen_email)


@router.message(ParseScheduleByInterval.chosen_email)
async def choosing_email(message: Message, state: FSMContext):
    await state.update_data(chosen_email=message.text.lower())
    await message.answer("Great! Now choose interval, firstly with start date:",
                         reply_markup=await SimpleCalendar().start_calendar())
    await state.set_state(ParseScheduleByInterval.chosen_start_date)


@router.callback_query(ParseScheduleByInterval.chosen_start_date, SimpleCalendarCallback.filter())
async def choosing_start_date(call: CallbackQuery, callback_data: CallbackQuery, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if selected and date:
        await call.message.edit_text(f"You selected: {date.strftime('%Y-%m-%d')}")
        await state.update_data(chosen_start_date=date)
        await call.message.answer("Awesome! Now choose end date:",
                                  reply_markup= await SimpleCalendar().start_calendar())
        await state.set_state(ParseScheduleByInterval.chosen_end_date)


@router.callback_query(ParseScheduleByInterval.chosen_end_date, SimpleCalendarCallback.filter())
async def choosing_start_date(call: CallbackQuery, callback_data: CallbackQuery, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if selected and date:
        user_data = await state.get_data()
        await call.message.edit_text(f"You selected: {date.strftime('%Y-%m-%d')}")
        if abs(date - user_data['chosen_start_date']).days >= 30:
            await call.message.answer("Sorry, interval only for 30 or less days")
            await state.clear()
            return
        email = user_data['chosen_email']
        if '@kse.org.ua' not in email:
            email += '@kse.org.ua'

        subjects = parser.parse_students_subjects(email)

        if not subjects:
            await call.message.answer("No schedule found by given email")
            await state.clear()
            return

        if date < user_data['chosen_start_date']:
            schedule = parser.get_interval_subjects_from_schedule(subjects, date, user_data['chosen_start_date'])
        else:
            schedule = parser.get_interval_subjects_from_schedule(subjects, user_data['chosen_start_date'], date)

        formated_schedule = parser.format_schedule(schedule)

        if not formated_schedule:
            await call.message.answer("<b>No schedule found by given email and interval</b>")
        else:
            if len(formated_schedule) > 4000:
                formated_schedule = parser.compact_format_schedule(schedule)
                if len(formated_schedule) > 4000:
                    await call.message.answer(f"<b>Schedule is too long, try to change interval</b>", parse_mode=ParseMode.HTML)
                    await state.clear()
                    return
                await call.message.answer(f"Schedule for <b>{email}</b>\n\n" + formated_schedule, parse_mode=ParseMode.HTML)
            await call.message.answer(f"Schedule for <b>{email}</b>\n\n" + formated_schedule, parse_mode=ParseMode.HTML)
        await state.clear()
