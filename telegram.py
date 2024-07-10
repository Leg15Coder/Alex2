from main import alex
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import CommandObject
from config import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.alex_tg_token.get_secret_value(), parse_mode="HTML")
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("hi")


@dp.message()
async def answer(message: types.Message):
    answ = alex.answer(message.text)
    await message.answer(str(answ) + '.')


async def main():
    await dp.start_polling(bot)

asyncio.run(main())
