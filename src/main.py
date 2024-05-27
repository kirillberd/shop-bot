import asyncio
import logging
import sys
from os import getenv
from aiogram import Dispatcher
from dotenv import load_dotenv
from handlers.registration_handlers import registration_router
from handlers.keyboard_handlers import keyboard_router
from storage.storage import MongoStorage
from handlers.admin_handlers import admin_router
load_dotenv()

storage = MongoStorage(getenv('DB_URI'), getenv('DB_NAME'), getenv('COLLECTION_NAME'))

dp = Dispatcher(storage=storage)
dp.include_router(registration_router)
dp.include_router(keyboard_router)
dp.include_router(admin_router)

async def main():
    from bot.bot import bot
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())