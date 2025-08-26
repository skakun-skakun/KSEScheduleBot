from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot import parser

from keyboards.adj_week_kb import adj_week_kb

from states.ParseScheduleByWeek import ParseScheduleByWeek

router = Router()


@router.message(StateFilter(None), Command('week_schedule'))
async def week_schedule_ask_email(message: Message, state: FSMContext):
    await message.answer("Enter email (without @kse.org.ua):")
    await state.set_state(ParseScheduleByWeek.chosen_email)


@router.message(ParseScheduleByWeek.chosen_email)
async def choosing_email(message: Message, state: FSMContext):
    await state.update_data(chosen_email=message.text.lower())
    await message.answer("Great! Now enter week number (number from 1 to a lot):")
    await state.set_state(ParseScheduleByWeek.choosen_week)


@router.message(ParseScheduleByWeek.choosen_week)
async def choosing_week(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Please enter a positive number")
        return
    if int(message.text) <= 0:
        await message.answer("Please enter a positive number")
        return

    user_data = await state.get_data()
    email = user_data['chosen_email']
    if '@kse.org.ua' not in email:
        email += '@kse.org.ua'

    subjects = parser.parse_students_subjects(email)
    if not subjects:
        await message.answer("No schedule found by given email")
        await state.clear()
        return

    schedule = parser.get_week_subjects_from_schedule(subjects, int(message.text))

    formated_schedule = parser.format_schedule(schedule)

    if not formated_schedule:
        await message.answer("<b>No schedule found by given email and interval</b>")
    else:
        if len(formated_schedule) > 3500:
            formated_schedule = parser.compact_format_schedule(schedule)
            if len(formated_schedule) > 3500:
                await message.answer(f"<b>Schedule is too long, try to change interval</b>",
                                     parse_mode=ParseMode.HTML)
                await state.clear()
                return
            await message.answer(f"Schedule for <b>{email}</b> for <b>Week {message.text}</b>\n\n" + formated_schedule,
                                 parse_mode=ParseMode.HTML, reply_markup=adj_week_kb(email, int(message.text)))
        await message.answer(f"Schedule for <b>{email}</b> for <b>Week {message.text}</b>\n\n" + formated_schedule,
                             parse_mode=ParseMode.HTML, reply_markup=adj_week_kb(email, int(message.text)))
    await state.clear()


@router.callback_query(StateFilter(None), F.data.startswith("week_schedule`"))
async def inline_week_schedule(call: CallbackQuery, state: FSMContext):
    _, email, week = call.data.split("`")
    subjects = parser.parse_students_subjects(email)
    if not subjects:
        await call.message.edit_text("No schedule found by given email")
        await call.message.edit_reply_markup(reply_markup=adj_week_kb(email, int(week)))
        await state.clear()
        return

    schedule = parser.get_week_subjects_from_schedule(subjects, int(week))

    formated_schedule = parser.format_schedule(schedule)

    if not formated_schedule:
        await call.message.edit_text("<b>No schedule found by given email and interval</b>",
                                     parse_mode=ParseMode.HTML)
        await call.message.edit_reply_markup(reply_markup=adj_week_kb(email, int(week)))
    else:
        if len(formated_schedule) > 3500:
            formated_schedule = parser.compact_format_schedule(schedule)
            if len(formated_schedule) > 3500:
                await call.message.edit_text(f"<b>Schedule is too long, try to change interval</b>",
                                     parse_mode=ParseMode.HTML)
                await call.message.edit_reply_markup(reply_markup=adj_week_kb(email, int(week)))
                await state.clear()
                return
            await call.message.edit_text(f"Schedule for <b>{email}</b> for <b>Week {week}</b>\n\n" + formated_schedule,
                                         parse_mode=ParseMode.HTML)
            await call.message.edit_reply_markup(reply_markup=adj_week_kb(email, int(week)))

        await call.message.edit_text(f"Schedule for <b>{email}</b> for <b>Week {week}</b>\n\n" + formated_schedule,
                                     parse_mode=ParseMode.HTML)
        await call.message.edit_reply_markup(reply_markup=adj_week_kb(email, int(week)))
    await state.clear()
