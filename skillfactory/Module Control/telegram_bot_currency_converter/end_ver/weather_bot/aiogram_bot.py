import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.methods.send_message import SendMessage

from config import tg_bot_token, open_weather_token


bot = Bot(token=tg_bot_token)

# Dispatcher is a root router
dp = Dispatcher()

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("напиши город")

# And the run events dispatching
await dp.start_polling(bot)

if __name__ == '__main__':
    executor.start_polling(dp)