# """from codecs import replace_errors
#
# from aiogram import  Router, F
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.types import (
#     Message,
#     CallbackQuery,
#     ReplyKeyboardMarkup,
#     KeyboardButton,
#     InlineKeyboardMarkup,
#     InlineKeyboardButton,
# )
# from forms.user import Form
# from aiogram.fsm.context import FSMContext
# import aiosqlite
#
#
# router = Router()
#
# #-------------------DB-------------------
# """
# DB_NAME = "movies.db"
#
# async def init_db():
#     async with aiosqlite.connect(DB_NAME) as db:
#         await db.execute("""
#             CREATE TABLE IF NOT EXISTS movies (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             title TEXT,
#             type TEXT,
#             year INTEGER,
#             release_date TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#             """)
#         await db.commit()
#
# async def add_movie(title, type, year, release_date):
#     async with aiosqlite.connect(DB_NAME) as db:
#         await db.execute("""
#             INSERT INTO movies (title, type, year, release_date)
#             VALUES (?, ?, ?, ?)
#         """, (title, type, year, release_date))
#         await db.commit()
#
# async def get_movies():
#     async with aiosqlite.connect(DB_NAME) as db:
#         cursor = await db.execute("SELECT * FROM movies")
#         result = await cursor.fetchall()
#         return result
#
# #-------------------DB-------------------
#
#
# @router.message(Command("start"))
# async def start(message: Message):
#     await init_db()
#     await message.answer("Create an account\nEnter /reg AGE ")
#
# @router.message(Command("reg"))
# async def reg(message: Message):
#     parts = message.text.strip().split()
#
#     if len(parts) != 2 or not parts[1].isdigit():
#         await message.answer("Enter the command correctly")
#         return
#
#     await add_movies(message.from_user.title, int(parts[1]))
#
#     await message.answer("Success")
#
# @router.message(Command("users"))
# async def reg(message: Message):
#     movie = await get_movies()
#
#     if not movies:
#         await message.answer("No movies found")
#         return
#     text = "Movies in base:\n\n"
#     for title, type, year, release_date, created_at in movies:
#         text += f"*{title}\n - {type}\n - {year}\n - {release_date}\n - {created_at}*"
#
#     await message.answer(text, parse_mode="Markdown")
#
# #---------------------------------------------------------------------------------------------------------
#
# async def init_db_users():
#     async with aiosqlite.connect(DB_NAME) as db:
#         await db.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             telegram_id INTEGER UNIQUE,
#             login TEXT,
#             password TEXT
#             """)
#             await db.commit()
#
#
#
# async def add_user(title, type, year, release_date):
#     async with aiosqlite.connect(DB_NAME) as db:
#         await db.execute("""
#             INSERT INTO users (title, type, year, release_date)
#             VALUES (?, ?, ?, ?)
#         """, (title, type, year, release_date))
#         await db.commit()
#
#
#
#
# """
# @router.message(Command("start"))
# async def start(message: Message, state: FSMContext):
#     await message.answer("Create an account\nEnter login: ")
#     await state.set_state(Form.login)
#
# @router.message(Command("cancel"))
# async def process_form(message: Message, state: FSMContext):
#     await message.clear()
#     await message.answer("Cancel")
#
# @router.message(Form.login, F.text)
# async def process_login(message: Message, state: FSMContext):
#     await state.update_data(login=message.text)
#
#     await message.answer(f"Hello {message.text}\nEnter a password: ")
#     await state.set_state(Form.pas)
#
# @router.message(Form.pas, F.text)
# async def process_pas(message: Message, state: FSMContext):
#     pas_text = message.text
#     if len(pas_text) < 2 or len(pas_text) > 10:
#         await message.answer("Error pas")
#         return
#
#     await state.update_data(pas=pas_text)
#
#     data = await state.get_data()
#     login = data["login"]
#     pas = data["pas"]
#
#     await message.answer(f"Success\nLogin: {login} \nPassword: {pas}")
#     await state.clear()
# """
#
#
#
#
#
#



 # def get_main_reply_keyboard():
 #     keyboard = ReplyKeyboardMarkup(
 #         keyboard=[
 #             [KeyboardButton(text="about bot")],
 #             [KeyboardButton(text="start"), KeyboardButton(text="help")]
 #         ],
 #         resize_keyboard=True
 #     )
 #     return keyboard
 #
 # def get_main_inline_keyboard():
 #     keyboard = InlineKeyboardMarkup(
 #         inline_keyboard=[
 #             [InlineKeyboardButton(text="open", url="https://telegram.org")],
 #             [InlineKeyboardButton(text="add", callback_data="info_more"),
 #              InlineKeyboardButton(text="delete", callback_data="info_more")]
 #             ]
 #     )
 #
 #     return keyboard
 #
 # @router.callback_query(lambda c: c.data == "info_more")
 # async def info_more(callback):
 #     await callback.message.answer("more info")
 #     await callback.answer()
 #
 # @router.message(Command("start"))
 # @router.message(F.text.lower() == "start")
 # async def start(message: Message):
 #     await message.answer("Hi\n\n/help\n/about")
 #
 # @router.message(Command("help"))
 # @router.message(F.text.lower() == "help")
 # async def helps(message: Message):
 #     await message.answer("Commands: \n*/help*\n*/start*\n*/about*", parse_mode="Markdown",
 #     reply_markup = get_main_reply_keyboard())
 #
 # @router.message(Command("about"))
 # @router.message(F.text.lower() == "about bot")
 # async def about(message: Message):
 #     await message.answer("about bot", reply_markup=get_main_inline_keyboard())
 #
 # @router.message()
 # async def mess(message: Message):
 #     await message.answer("Text")
