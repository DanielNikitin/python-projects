import requests
import datetime
from config import bot_token, open_weather_token
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter

bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(F.text == '/start')
async def start_commands(message: Message):
    await message.reply("yo")

@dp.message()
async def get_weather(message: types.Message):
    try:
        # формируем запрос requests.get (получить)
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        current_weater = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])


        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f"City: {city}\n Temperature: {current_weater}\n"
              f"Humidity: {humidity}%\n Davlenie: {pressure}kP\n"
              f"Wind: {wind}m/s\n Sunrise: {sunrise_timestamp}\n"
              f"Sunset: {sunset_timestamp}\n"
              f"Prodolzitelnost dna: {length_of_the_day}")

    except:
        await message.reply("\U00002620 check city name \U00002620")

# Polling, т.е бесконечный цикл проверки апдейтов
async def main():
    await dp.start_polling(bot)

# Функция main() запускается только в случае если скрипт запущен с этого файла
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')