import asyncio
import logging
import sys
from aiogram.enums import ParseMode
from os import getenv
from aiogram import Bot
from aiogram import Dispatcher
from dotenv import load_dotenv
from handlers.registration_handlers import registration_router
from storage.storage import MongoStorage
load_dotenv()

storage = MongoStorage(getenv('DB_URI'), getenv('DB_NAME'), getenv('COLLECTION_NAME'))

dp = Dispatcher(storage=storage)
dp.include_router(registration_router)

async def main():
    bot = Bot(token=getenv('BOT_TOKEN'), parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())