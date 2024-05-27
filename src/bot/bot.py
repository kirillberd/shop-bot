from aiogram import Bot
from os import getenv
from dotenv import load_dotenv
from aiogram.enums import ParseMode
load_dotenv()
bot = bot = Bot(token=getenv('BOT_TOKEN'), parse_mode=ParseMode.HTML)