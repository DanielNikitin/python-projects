import requests
from config import tg_bot_token, open_weather_token
from pprint import pprint
import datetime

def get_weather(city, open_weather_token):
    try:
        # фомируем запрос requests.get (получить)
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        #pprint(data)

        city = data["name"]
        current_weater = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])


        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f"Gorod: {city}\n Temperature: {current_weater}\n"
              f"Vlaznost: {humidity}%\n Davlenie: {pressure}kP\n"
              f"Veter: {wind}m/s\n Voshod Solnca: {sunrise_timestamp}\n"
              f"Zakat Solnca: {sunset_timestamp}\n"
              f"Prodolzitelnost dna: {length_of_the_day}")

    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def main():
    city = input("...: ")
    get_weather(city, open_weather_token)

if __name__ == '__main__':
    main()