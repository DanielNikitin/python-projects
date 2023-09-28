from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)

main_kb = [
    [KeyboardButton(text='1'),
     KeyboardButton(text='/myid')],
    [KeyboardButton(text='Maintenance'),
     KeyboardButton(text='Прочее')]
          ]

main = ReplyKeyboardMarkup(keyboard=main_kb,
                           resize_keyboard=True,
                           input_field_placeholder='daily customs garage © 2023')

# --------------

other_kb = [
    [KeyboardButton(text='Currency Converter')],
           ]

other = ReplyKeyboardMarkup(keyboard=other_kb,
                            resize_keyboard=True)

# --------------

converter_kb = [
    [KeyboardButton(text='EUR TO USD')],
     [KeyboardButton(text='USD TO EUR')],
    [KeyboardButton(text='Другой Вариант'),
     KeyboardButton(text='Доступные валюты')]
                ]

converter = ReplyKeyboardMarkup(keyboard=converter_kb)

# --------------

socials_kb = [
    [InlineKeyboardButton(text='Telegram', url='')],
    [InlineKeyboardButton(text='Youtube', url='')]
             ]

socials = InlineKeyboardMarkup(inline_keyboard=socials_kb)

# --------------

maintenance_kb = [
    [KeyboardButton(text='JIG Calib'),
     KeyboardButton(text='Cut')]
           ]

maintenance = ReplyKeyboardMarkup(keyboard=maintenance_kb,
                            resize_keyboard=True)