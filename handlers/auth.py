from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from forms.app_states import AppState
from keyboards.menu import get_main_reply_menu , get_current_user

from database import add_user

router = Router()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(AppState.main)
    user = await get_current_user(message)
    if user:
        await message.answer("You are already logged in\nChoose section",
                             reply_markup=get_main_reply_menu())
        return
    await message.answer("Create an account\nEnter login: ")
    await state.set_state(AppState.login)

@router.message(AppState.login)
async def process_login(message: Message, state: FSMContext):
    login = (message.text or "").strip()
    if len(login) < 3 or len(login) > 32:
        await message.answer("Login must be 3-32 chars")
        return
    await state.update_data(login=login)
    await message.answer("Enter your password")
    await state.set_state(AppState.pas)

@router.message(AppState.pas)
async def process_password(message: Message, state: FSMContext):
    data = await state.get_data()
    login = data.get("login")
    password = (message.text or "").strip()

    if not login:
        await state.set_state(AppState.login)
        await message.answer("Enter login first")
        return
    if len(password) < 6 or len(password) > 64:
        await message.answer("Password must be 6-64 chars")
        return

    created = await add_user(
        telegram_id=message.from_user.id,
        login=login,
        password=password,
    )
    if not created:
        await state.set_state(AppState.main)
        await message.answer(
            "You are already registered\nChoose section",
            reply_markup=get_main_reply_menu(),
        )
        return

    await state.set_state(AppState.main)
    await message.answer("Successful\nYou have been logged in\nChoose section",
                         reply_markup=get_main_reply_menu())





# @router.message(Command("cancel"))
# async def process_log(message: Message, state: FSMContext):
#     await message.clear()
#     await message.answer("Cancel")
#
#
#
#     await message.answer(f"Hello {message.text}\nEnter a password: ")
#     await state.set_state(AppState.pas)
#
# @router.message(AppState.pas, F.text)
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
