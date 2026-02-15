from aiogram import Router, F
from aiogram.types import Message, CallbackQuery , ReplyKeyboardRemove
from keyboards.menu import get_main_reply_movies, get_current_user, get_main_reply_menu
from database import get_movies, delete_movie, add_movie, get_user_by_telegram_id
from forms.app_states import AppState
from aiogram.fsm.context import FSMContext


router = Router()

MOVIES_PER_PAGE = 15

@router.message(AppState.main, F.text.lower() == "movies")
async def movies_menu(message: Message, state: FSMContext):
    await state.set_state(AppState.movies_menu)
    await message.answer(
        "Movies section",
        reply_markup=get_main_reply_movies()
    )

@router.message(AppState.movies_menu, F.text.lower() == "add movie")
async def add_movie_start(message: Message, state: FSMContext):
    await state.set_state(AppState.add_movie_title)
    await message.answer("Enter name", reply_markup=ReplyKeyboardRemove())

@router.message(AppState.add_movie_title)
async def movie_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AppState.add_movie_type)
    await message.answer("M | S", reply_markup=ReplyKeyboardRemove())

@router.message(AppState.add_movie_type)
async def movie_type(message: Message, state: FSMContext):
    await state.update_data(type_=message.text)
    await state.set_state(AppState.add_movie_comment)
    await message.answer("comment:", reply_markup=ReplyKeyboardRemove())

@router.message(AppState.add_movie_comment)
async def movie_comment(message: Message, state: FSMContext):
    data = await state.get_data()

    title = data["title"]
    type_ = data["type_"]
    comment = message.text

    user = await get_current_user(message)

    await add_movie(user[0], title, type_, comment)

    await message.answer("✅")

    await state.clear()
    await state.set_state(AppState.movies_menu)
    await message.answer(
        "Movies section",
        reply_markup=get_main_reply_movies()
    )

@router.message(AppState.movies_menu, F.text.lower() == "list movies")
async def list_movies_handler(message: Message, state: FSMContext):
    user = await get_current_user(message)
    if not user:
        await message.answer("error(list) /start")
        return

    movies = await get_movies(user[0])
    if not movies:
        await message.answer("list empty")
        return

    text = "Movies list:\n\n"

    movie_map = {}

    for index, movie in enumerate(movies, start=1):
        movie_id, user_id, title, type_, comment, created_at = movie
        text += f"{index}. {title} ({type_}) — {comment}\n"
        movie_map[index] = movie_id

    await state.update_data(movie_map=movie_map)

    await message.answer(text)

@router.message(AppState.movies_menu, F.text.lower() == "del movie")
async def delete_start(message: Message, state: FSMContext):
    await state.set_state(AppState.delete_movie_number)
    await message.answer("Enter number to delete:")

@router.message(AppState.delete_movie_number)
async def delete_by_number(message: Message, state: FSMContext):
    data = await state.get_data()
    movie_map = data.get("movie_map")

    if not movie_map:
        await message.answer("First use 'list movies'")
        await state.set_state(AppState.movies_menu)
        return

    try:
        number = int(message.text)
    except ValueError:
        await message.answer("Enter a valid number")
        return

    if number not in movie_map:
        await message.answer("No movie with that number")
        return

    movie_id = movie_map[number]
    user = await get_current_user(message)

    await delete_movie(user[0], movie_id)

    await message.answer("✅ Deleted")

    await state.set_state(AppState.movies_menu)

@router.message(AppState.movies_menu, F.text.lower() == "back")
async def back_handler(message: Message, state: FSMContext):
    await state.set_state(AppState.main)
    await message.answer("Main menu", reply_markup=get_main_reply_menu())

#-------------------------------------------------------------------------------------

@router.callback_query(F.data.startswith("del_movie_"))
async def delete_callback(callback: CallbackQuery):
    movie_id = int(callback.data.split("_")[2])
    user = await get_user_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer("error(user not found)m /start")
        return
    await delete_movie(user[0], movie_id)

    await callback.message.edit_text("Successful")
    await callback.answer()