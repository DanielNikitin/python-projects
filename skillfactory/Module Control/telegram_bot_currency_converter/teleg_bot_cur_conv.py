import telebot  # я выбрал его так как уже работал с ним, мне так удобнее
from telebot import types  # чтобы не обращаться к types через telebot, делаю импорт модуля напрямую
from currency_converter import CurrencyConverter  # https://pypi.org/project/CurrencyConverter/

bot = telebot.TeleBot('6477563848:AAHS2OiKnKFPadIl-ThW5Q0xzzfrSXmkeq0')  # botfather токен
currency = CurrencyConverter()  # подключение функционала библиотеки
amount = 0  # переменная для хранения валютной единицы пользователя


@bot.message_handler(commands=['start'])  # ожидание ввода /start
def menu(message):
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, input_amount)

    markup = types.InlineKeyboardMarkup(row_width=2)  # вывод по 2 кнопки в строчку
    btn1 = types.InlineKeyboardButton('💶EUR/USD💵', callback_data='eur/usd')
    btn2 = types.InlineKeyboardButton('💵USD/EUR💶', callback_data='usd/eur')
    btn3 = types.InlineKeyboardButton('EUR/GBP🇬🇧', callback_data='eur/gbp')
    btn4 = types.InlineKeyboardButton('❓Другая❓', callback_data='other')
    btn5 = types.InlineKeyboardButton('-->Варианты валют<--', callback_data='values')
    markup.add(btn1, btn2, btn3, btn4, btn5)  # 5 кнопок по (row_width=2)

    bot.send_message(message.chat.id, '🤗 *** ДОБРО ПОЖАЛОВАТЬ *** 🤗')
    bot.send_message(message.chat.id, '🏦ВАЛЮТНЫЙ БОТ КОНВЕРТЕР🏦')
    bot.send_message(message.chat.id, '♦️️♦️♦️️️️️️️НАШЕ МЕНЮ♦️️️♦️️♦️')
    bot.send_message(message.chat.id, '👇👇👇👇👇👇👇👇👇👇👇👇', reply_markup=markup)  # markup для вывода кнопок

    message: False  # отключаем ЭХО после вывода меню


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if '/' in call.data:  # пользователь нажал на кнопку
        # Если пользователь нажал на кнопку с валютной парой
        values = call.data.upper().split('/')  #
        if len(values) >= 2:
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(call.message.chat.id, f'Итог: {round(res, 2)} \n'
                                                   f'Введите новую сумму')
            bot.register_next_step_handler(call.message, input_amount)

    elif call.data == 'other':
        # Если пользователь выбрал 'Другое''
        bot.send_message(call.message.chat.id, 'Введите значение:')
        bot.register_next_step_handler(call.message, input_amount)

    elif call.data == 'values':
        # Если пользователь выбрал 'Варианты Валют'
        bot.send_message(call.message.chat.id, 'Japan Yen 🇯🇵 :  JPY\nTurkish Lir 🇹🇳 :  TRY')

    else:
        # Если нажата неизвестная кнопка
        bot.send_message(call.message.chat.id, 'callback: None')
        bot.register_next_step_handler(call.message, input_amount)

def input_amount(message):  # ввод валюты
    global amount
    try:
        amount = int(message.text.strip())  # текст в запрашиваемую Единицу Валюты
    except ValueError:
        bot.send_message(message.chat.id, 'Введите цифрами кол-во желаемых единиц')
        bot.register_next_step_handler(message, input_amount)  # ожидание ввода валютных единиц
        return

@bot.message_handler(func=lambda message: True)  # ожидаем любой ввод пользователя
def text_handler(message):  # слушаем любые сообщения
    bot.send_message(message.chat.id, "Для получения МЕНЮ\nНажмите кнопку --> /start")

bot.polling(none_stop=True)  # запуск цикла работы бота