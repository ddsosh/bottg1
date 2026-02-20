from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards.menu import get_main_reply_notes, get_main_reply_menu, get_current_user
from database import get_user_by_telegram_id, delete_note, get_notes, add_note
from forms.app_states import AppState


router = Router()


@router.message(AppState.main, F.text.lower() == "notes")
async def notes_menu(message: Message, state: FSMContext):
    await state.set_state(AppState.notes_menu)
    await message.answer("Notes section", reply_markup=get_main_reply_notes())


@router.message(AppState.notes_menu, F.text.lower() == "add note")
async def add_note_start(message: Message, state: FSMContext):
    await state.set_state(AppState.add_note_title)
    await message.answer("name", reply_markup=ReplyKeyboardRemove())


@router.message(AppState.add_note_title)
async def note_title(message: Message, state: FSMContext):
    title = (message.text or "").strip()
    if not title:
        await message.answer("Title cannot be empty")
        return
    if len(title) > 50:
        await message.answer("Title is too long (max 50)")
        return

    await state.update_data(title=title)
    await state.set_state(AppState.add_note_date)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Skip", callback_data="skip_note_date")]]
    )
    await message.answer("Enter date or press Skip", reply_markup=keyboard)


@router.message(AppState.add_note_date)
async def note_date(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")

    if not title:
        await state.set_state(AppState.add_note_title)
        await message.answer("Enter title first")
        return

    raw_date = (message.text or "").strip()
    due_date = None if raw_date.lower() == "skip" else raw_date
    if due_date is not None and len(due_date) > 64:
        await message.answer("Date value is too long (max 64)")
        return

    user = await get_current_user(message)
    if not user:
        await state.set_state(AppState.main)
        await message.answer("error(user not found) /start", reply_markup=get_main_reply_menu())
        return

    await add_note(user[0], title, due_date)
    await message.answer("OK")

    await state.clear()
    await state.set_state(AppState.notes_menu)
    await message.answer("Notes section", reply_markup=get_main_reply_notes())


@router.message(AppState.notes_menu, F.text.lower() == "list notes")
async def list_note_handler(message: Message, state: FSMContext):
    user = await get_current_user(message)
    if not user:
        await message.answer("error(list) /start")
        return

    notes = await get_notes(user[0])
    if not notes:
        await message.answer("list empty")
        return

    text = "Notes:\n"
    note_map = {}

    for index, note in enumerate(notes, start=1):
        note_id, user_id, title, due_date, created_at = note
        date_text = due_date if due_date else "No date"
        text += f"{index}. {title} - {date_text}\n"
        note_map[index] = note_id

    await state.update_data(note_map=note_map)
    await message.answer(text)


@router.message(AppState.notes_menu, F.text.lower() == "del note")
async def delete_start(message: Message, state: FSMContext):
    await state.set_state(AppState.delete_note_number)
    await message.answer("Enter number to delete:", reply_markup=ReplyKeyboardRemove())


@router.message(AppState.delete_note_number)
async def delete_by_number(message: Message, state: FSMContext):
    data = await state.get_data()
    note_map = data.get("note_map")

    if not note_map:
        await message.answer("First use 'list notes'")
        await state.set_state(AppState.notes_menu)
        return

    try:
        number = int(message.text)
    except (TypeError, ValueError):
        await message.answer("Enter a valid number")
        return

    if number not in note_map:
        await message.answer("No note with that number")
        return

    note_id = note_map[number]
    user = await get_current_user(message)
    if not user:
        await state.set_state(AppState.main)
        await message.answer("error(user not found) /start", reply_markup=get_main_reply_menu())
        return

    await delete_note(user[0], note_id)
    await message.answer("OK Deleted")
    await state.set_state(AppState.notes_menu)


@router.callback_query(F.data.startswith("del_note_"))
async def delete_callback(callback: CallbackQuery):
    note_id = int(callback.data.split("_")[2])
    user = await get_current_user(callback)
    if not user:
        await callback.answer("error(user not found) /start")
        return

    await delete_note(user[0], note_id)
    await callback.message.edit_text("Successful")
    await callback.answer()


@router.callback_query(AppState.add_note_date, F.data == "skip_note_date")
async def skip_note_date(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")

    if not title:
        await state.set_state(AppState.add_note_title)
        await callback.message.answer("Enter title first")
        await callback.answer()
        return

    user = await get_current_user(callback)

    if not user:
        await state.set_state(AppState.main)
        await callback.message.answer("error(user not found) /start", reply_markup=get_main_reply_menu())
        await callback.answer()
        return

    await add_note(user[0], title, None)
    await callback.message.edit_text("OK Note saved without date")
    await callback.answer()

    await state.clear()
    await state.set_state(AppState.notes_menu)
    await callback.message.answer("Notes section", reply_markup=get_main_reply_notes())


@router.message(AppState.notes_menu, F.text.lower() == "back")
async def back_handler(message: Message, state: FSMContext):
    await state.set_state(AppState.main)
    await message.answer("Main menu", reply_markup=get_main_reply_menu())
