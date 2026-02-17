from aiogram import Router
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from database import get_user_by_telegram_id

router = Router()


def get_main_reply_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="movies"), KeyboardButton(text="notes")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_reply_movies():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="add movie"), KeyboardButton(text="list movies")],
            [KeyboardButton(text="del movie"), KeyboardButton(text="back")],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_reply_notes():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="add note"), KeyboardButton(text="list notes")],
            [KeyboardButton(text="del note"), KeyboardButton(text="back")],
        ],
        resize_keyboard=True
    )
    return keyboard


def get_main_inline_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1", url="https://telegram.org")],
            [InlineKeyboardButton(text="2", callback_data="info_more"),
             InlineKeyboardButton(text="3", callback_data="info_more")]
        ]
    )
    return keyboard

async def get_current_user(message: Message):
    return await get_user_by_telegram_id(message.from_user.id)

# ------------------------------------------------

