import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types, Dispatcher, executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)  # тот кто принимает сообщения

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("напиши город")


if __name__ == '__main__':
    executor.start_polling(dp)
