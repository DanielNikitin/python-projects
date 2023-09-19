from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter

import requests, json
from app.config import CURR_API, LAT_API

import app.keyboards as kb

# Рутер это 'поисковик' среди директорий
router = Router()

# Словари
chat_data = {}
user_states = {}

@router.message(F.text == '/start')
async def start(message: Message):
    await message.answer('Welcome to the DCG Bot!', reply_markup=kb.main)
    await message.answer('Нажмите на любую кнопку из Меню')


@router.message(F.text == 'EUR TO USD')
async def eur_to_usd(message: Message):
    await message.answer('EUR TO USD')
    from_currency = str('EUR')
    to_currency = str('USD')
    amount = float('1')

    responce = requests.get(
        f"{LAT_API}?amount={amount}&from={from_currency}&to={to_currency}")
    await message.answer(f"{amount} {from_currency} is {round(responce.json()['rates'][to_currency], 2)} {to_currency}")

@router.message(F.text == 'USD TO EUR')
async def usd_to_eur(message: Message):
    await message.answer('USD TO EUR')
    from_currency = str('USD')
    to_currency = str('EUR')
    amount = float('1')

    responce = requests.get(
        f"{LAT_API}?amount={amount}&from={from_currency}&to={to_currency}")
    await message.answer(f"{amount} {from_currency} is {round(responce.json()['rates'][to_currency], 2)} {to_currency}")


@router.message(F.text == 'Другой Вариант')
async def handle_input(message: Message):
    # Устанавливаем состояние пользователя в ожидание ввода
    user_states[message.chat.id] = "waiting_for_input"
    await message.answer("Введите данные для конвертации:\n[валюта 1] [валюта 2] [сумма]")

@router.message(lambda message: user_states.get(message.chat.id) == "waiting_for_input")
async def start_input(message: Message):
    user_state = user_states.get(message.chat.id)
    try:
        # если пользователь ожидает ввод
        if user_state == "waiting_for_input":
            # message.text записываем в input data
            input_data = message.text.split()
            # input data должна состоять из 3 основных переменных
            if len(input_data) == 3:
                # base (to currency)
                # quote (from_currency)
                quote, base, amount = input_data
                quote = quote.upper()  # ставим верхний регистр
                base = base.upper()
                try:
                    amount = float(amount)  # записываем значение
                    # делаем requests запрос по заданному API
                    responce = requests.get(
                        f"{LAT_API}?amount={amount}&from={quote}&to={base}")
                    result = f"{amount} {quote} is {round(responce.json()['rates'][base], 2)} {base}"
                    await message.answer(f"Result: {result}")

                    # Отправляем меню с кнопками
                    await message.answer("Выберите следующее действие:", reply_markup=kb.main)

                except ValueError:
                    await message.reply("Ошибка: Неверный формат суммы")
            else:
                await message.reply("Формат ввода:\n[eur] [usd] [100]")

                    # ****** ДОРАБОТАТЬ ********
        #user_states[message.chat.id] = None  # Сбрасываем состояние пользователя

    except Exception as e:
        await message.reply("Неверный ввод.\n Формат ввод: [eur] [usd] [100]")
        print(e)

@router.message(F.text == 'Доступные валюты')
async def data_currency(message: Message):
    response = requests.get(CURR_API)  # получаем (get) данные от curr_api
    data = response.json()  # получаем ответ от сервера в формате json, и преобразуем его в python код

    # Сортируем словарь по ключам (кодам валют) и сохраняем всё в новую переменную
    sorted_data = dict(sorted(data.items()))

    # Создаем столбец, содержащую все доступные валюты
    currency_list = '\n'.join([f'"{currency_code}": "{currency_name}"' for currency_code, currency_name in sorted_data.items()])

    # Отправляем столбец как одно сообщение
    await message.answer(currency_list)


# Хэндлер без фильтра, сработает, если ни один выше не сработает.
@router.message()
async def welcome(message: Message):
    await message.answer('Press to -> /start')