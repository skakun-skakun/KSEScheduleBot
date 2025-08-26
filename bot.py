import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from parser import Parser

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

parser = Parser()
