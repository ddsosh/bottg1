from aiogram import Router, F
from aiogram.types import (Message,
                           CallbackQuery,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardRemove)
from keyboards.menu import (get_main_reply_notes,
                            get_main_reply_menu,
                            get_current_user)
from database import get_user_by_telegram_id, delete_note, get_notes, add_note
from forms.app_states import AppState
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(AppState.main, F.text.lower() == "notes")
async def notes_menu(message: Message , state: FSMContext):
    await state.set_state(AppState.notes_menu)
    await message.answer(
        "Notes section",
        reply_markup=get_main_reply_notes()
    )

@router.message(AppState.notes_menu, F.text.lower() == "add note")
async def add_note_start(message: Message, state: FSMContext):
    await state.set_state(AppState.add_note_title)
    await message.answer("name", reply_markup=ReplyKeyboardRemove())

@router.message(AppState.add_note_title)
async def note_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AppState.add_note_date)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Skip",
                    callback_data="skip_note_date"
                )
            ]
        ]
    )

    await message.answer(
        "Enter date or press Skip",
        reply_markup=keyboard
    )

@router.message(AppState.add_note_date)
async def note_date(message: Message, state: FSMContext):
    data = await state.get_data()

    title = data["title"]
    if message.text.lower() == "skip":
        due_date = None
    else:
        due_date = message.text

    user = await get_current_user(message)

    await add_note(user[0], title, due_date)

    await message.answer("✅")

    await state.clear()
    await state.set_state(AppState.notes_menu)
    await message.answer(
        "Notes section",
        reply_markup=get_main_reply_notes()
    )

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

    text = "note:\n"

    note_map = {}

    for index, note in enumerate(notes, start=1):
        note_id, user_id, title, due_date, created_at = note
        text += f"{index}. {title} — {due_date}\n"

        note_map[index] = note_id

        date_text = due_date if due_date else "No date"
        await message.answer(
            f"{title}\n{date_text}",
            reply_markup=get_main_reply_notes())
        await state.update_data(note_map=note_map)

        await message.answer(text)

@router.message(AppState.notes_menu, F.text.lower() == "del note")
async def delete_start(message: Message, state: FSMContext):
    await state.set_state(AppState.delete_note_number)
    await message.answer("Enter number to delete:")

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
    except ValueError:
        await message.answer("Enter a valid number")
        return

    if number not in note_map:
        await message.answer("No note with that number")
        return

    note_id = note_map[number]
    user = await get_current_user(message)

    await delete_note(user[0], note_id)

    await message.answer("✅ Deleted")

    await state.set_state(AppState.notes_menu)

@router.callback_query(F.data.startswith("del note"))
async def delete_callback(callback: CallbackQuery):
    note_id = int(callback.data.split("_")[2])
    user = await get_user_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer("error(user not found)n /start")
        return
    await delete_note(user[0], note_id)

    await callback.message.edit_text("Successful")
    await callback.answer()

@router.callback_query(AppState.add_note_date, F.data == "skip_note_date")
async def skip_note_date(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    title = data["title"]

    user = await get_user_by_telegram_id(callback.from_user.id)

    await add_note(user[0], title, None)

    await callback.message.edit_text("✅ Note saved without date")
    await callback.answer()

    await state.clear()
    await state.set_state(AppState.notes_menu)

    await callback.message.answer(
        "Notes section",
        reply_markup=get_main_reply_notes()
    )


@router.message(AppState.notes_menu, F.text.lower() == "back")
async def back_handler(message: Message, state: FSMContext):
    await state.set_state(AppState.main)
    await message.answer("Main menu", reply_markup=get_main_reply_menu())

