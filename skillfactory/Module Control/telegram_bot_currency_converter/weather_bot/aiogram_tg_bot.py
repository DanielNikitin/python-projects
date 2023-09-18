import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types, Dispatcher, executor

bot = Bot(token=weather_bot_token)
dp = Dispatcher(bot)  # тот кто принимает сообщения

@dp.message_handler(commands=["start"])
async def start_commands(message: types.Message):
    await message.reply("yo")


@dp.message_handler()
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

if __name__ == '__main__':
    executor.start_polling(dp)