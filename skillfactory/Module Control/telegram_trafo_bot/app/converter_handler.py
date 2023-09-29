from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Filter

import app.keyboard as kb

conv_router = Router()

# Словари
chat_data = {}  # данные записанные пользователем в чат
user_states = {}  # состояние пользователя

#               CURRENCY CONVERTER                     #
#  **************************************************  #

@conv_router.message(F.text == 'Currency Converter')
async def converter(message: Message):
    await message.answer('...', reply_markup=kb.converter)

# Не возвращает в меню Конвертера после выбора Другое

@conv_router.message(F.text == 'EUR TO USD')
async def eur_to_usd(message: Message):
    await message.answer('EUR TO USD')
    user_states[message.chat.id] = None  # Сбрасываем состояние пользователя
    quote = str('EUR')
    base = str('USD')
    amount = float('1')

    responce = requests.get(
        f"{LAT_API}?amount={amount}&from={quote}&to={base}")
    await message.answer(f"{amount} {quote} is {round(responce.json()['rates'][base], 2)} {base}")

@conv_router.message(F.text == 'USD TO EUR')
async def usd_to_eur(message: Message):
    await message.answer('USD TO EUR')
    user_states[message.chat.id] = None  # Сбрасываем состояние пользователя
    quote = str('USD')
    base = str('EUR')
    amount = float('1')

    responce = requests.get(
        f"{LAT_API}?amount={amount}&from={quote}&to={base}")
    await message.answer(f"{amount} {quote} is {round(responce.json()['rates'][base], 2)} {base}")

@conv_router.message(F.text == 'Другой Вариант')
async def handle_input(message: Message):
    # Устанавливаем состояние пользователя в ожидание ввода
    user_states[message.chat.id] = "waiting_for_input"
    await message.answer("Введите данные для конвертации:\n[валюта 1] [валюта 2] [сумма]")

@conv_router.message(lambda message: user_states.get(message.chat.id) == "waiting_for_input")
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
                    # round нужен для округления результата с двумя значениями после запятой
                    result = f"{amount} {quote} is {round(responce.json()['rates'][base], 2)} {base}"
                    await message.answer(f"Result: {result}")

                    # Отправляем меню с кнопками
                    await message.answer("Выберите следующее действие:", reply_markup=kb.main)

                except ValueError:
                    await message.reply("Ошибка: Неверный формат суммы")
            else:
                # можно прикрутить ИИ чтобы пользователь не мог ошибиться в плане орфографии,
                # не выводить ошибку об 'битокоин' а дать возможность ИИ 'предполагать' вариант
                await message.reply("Формат ввода:\n[eur] [usd] [100]")

    except Exception as e:
        await message.reply("Неверный ввод.\n Формат ввод: [eur] [usd] [100]")
        print(e)

@conv_router.message(F.text == 'Доступные валюты')
async def data_currency(message: Message):
    response = requests.get(CURR_API)  # получаем (get) данные от curr_api
    data = response.json()  # получаем ответ от сервера в формате json, и преобразуем его в python код

    # Сортируем словарь по ключам (кодам валют) и сохраняем всё в новую переменную
    sorted_data = dict(sorted(data.items()))

    # Создаем столбец, содержащую все доступные валюты
    currency_list = '\n'.join([f'"{currency_code}": "{currency_name}"' for currency_code, currency_name in sorted_data.items()])

    # Отправляем столбец как одно сообщение
    await message.answer(currency_list)