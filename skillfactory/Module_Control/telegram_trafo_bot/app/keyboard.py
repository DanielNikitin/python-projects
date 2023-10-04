from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)

# /////////////////////////////////////////
# -------------- MAIN

def root_keyboard(user_id, root_id, maintenance_id):
    main_kb = [
        [KeyboardButton(text='Личные Расходы')],
        [KeyboardButton(text='My ID'),
        KeyboardButton(text='Прочее')],
        [KeyboardButton(text='Обновления')]
    ]

    if user_id in root_id:
        main_kb.insert(0, [KeyboardButton(text='Root')])

    if user_id in maintenance_id:
        main_kb.insert(1, [KeyboardButton(text='Maintenance')])

    return ReplyKeyboardMarkup(keyboard=main_kb,
                               resize_keyboard=True,
                               input_field_placeholder='daily customs garage © 2023')

# /////////////////////////////////////////
# -------------- OTHER --------------

other_kb = [
    [KeyboardButton(text='Currency Converter')],
    [KeyboardButton(text='Back')]
           ]

other = ReplyKeyboardMarkup(keyboard=other_kb,
                            resize_keyboard=True)

# -------------- CONVERTER --------------

converter_kb = [
    [KeyboardButton(text='EUR TO USD')],
    [KeyboardButton(text='USD TO EUR')],
    [KeyboardButton(text='Другой Вариант'),
     KeyboardButton(text='Доступные валюты')],
    [KeyboardButton(text='Back')]
                ]

converter = ReplyKeyboardMarkup(keyboard=converter_kb)

# /////////////////////////////////////////
# -------------- SOCIAL

socials_kb = [
    [InlineKeyboardButton(text='Telegram', url='')],
    [InlineKeyboardButton(text='Youtube', url='')]
             ]

socials = InlineKeyboardMarkup(inline_keyboard=socials_kb)

# /////////////////////////////////////////
# -------------- MAINTENANCE --------------

maintenance_kb = [
    [KeyboardButton(text='Jig Calibration'),
     KeyboardButton(text='Reserv')],
    [KeyboardButton(text='Back')]
           ]

maintenance = ReplyKeyboardMarkup(keyboard=maintenance_kb,
                            resize_keyboard=True)

# -------------- JIG

jig_kb = [
    [KeyboardButton(text='Ввести Модель Шаблона')],
    [KeyboardButton(text='Список Рабочих Мест')],
    [KeyboardButton(text='Список Шаблонов')],
    [KeyboardButton(text='Чертежи')],
    [KeyboardButton(text='Инструкция')],
    [KeyboardButton(text='Back')]
           ]

jig = ReplyKeyboardMarkup(keyboard=jig_kb,
                            resize_keyboard=True)

# //////////////////////////////////
# -------------- ROOT --------------

root_kb = [
    [KeyboardButton(text='Database Menu'),
     KeyboardButton(text='Reserv')],
    [KeyboardButton(text='Back')]
           ]

root = ReplyKeyboardMarkup(keyboard=root_kb,
                            resize_keyboard=True)

# -------------- Database Menu

database_menu_kb = [
    [KeyboardButton(text='Database')],
    [KeyboardButton(text='Table')],
    [KeyboardButton(text='Parts')],
    [KeyboardButton(text='Back')],
                    ]

database_menu = ReplyKeyboardMarkup(keyboard=database_menu_kb,
                            resize_keyboard=True)

# -------------- Database

database_kb = [
    [KeyboardButton(text='D.Add')],
    [KeyboardButton(text='D.List')],
    [KeyboardButton(text='D.Remove')],
    [KeyboardButton(text='Back')]
           ]

database = ReplyKeyboardMarkup(keyboard=database_kb,
                            resize_keyboard=True)

# -------------- Table

table_kb = [
    [KeyboardButton(text='T.Add')],
    [KeyboardButton(text='T.List')],
    [KeyboardButton(text='T.Remove')],
    [KeyboardButton(text='Back')]
           ]

table = ReplyKeyboardMarkup(keyboard=table_kb,
                            resize_keyboard=True)

# -------------- Parts

parts_kb = [
    [KeyboardButton(text='P.Add')],
    [KeyboardButton(text='P.List')],
    [KeyboardButton(text='P.Remove')],
    [KeyboardButton(text='Back')]
           ]

parts = ReplyKeyboardMarkup(keyboard=parts_kb,
                            resize_keyboard=True)