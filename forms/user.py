from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    login = State()
    pas = State()

if user:
    await message.answer(reply_markup=get_main_reply_notes())
    return