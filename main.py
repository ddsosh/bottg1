from os import getenv
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from database import init_db
from handlers.auth import router as auth_router
from handlers.movies import router as movies_router
from keyboards.menu import router as menu_router
from handlers.notes import router as notes_router

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()


async def main():
    bot = Bot(token=TOKEN)
    await init_db()
    dp.include_router(auth_router)
    dp.include_router(movies_router)
    dp.include_router(menu_router)
    dp.include_router(notes_router)
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())