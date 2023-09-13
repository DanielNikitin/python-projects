import telebot  # я выбрал его так как уже работал с ним, мне так удобнее
from telebot import types  # модуль для работы с интерфейсом
from currency_converter import CurrencyConverter  # https://pypi.org/project/CurrencyConverter/
import time

bot = telebot.TeleBot('6477563848:AAHS2OiKnKFPadIl-ThW5Q0xzzfrSXmkeq0')  # botfather токен
currency = CurrencyConverter()  # подключение функционала библиотеки
amount = 0  # переменная для хранения валютной единицы пользователя


@bot.message_handler(commands=['start'])  # ожидание ввода /start
def start(message):
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, input_amount)

def input_amount(message):  # ввод валюты
    global amount
    try:
        amount = int(message.text.strip())
        bot.send_message(message.chat.id, f'Вы хотите конвертировать {amount} единиц')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка 1')
        bot.register_next_step_handler(message, input_amount)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('💶EUR/USD💵', callback_data='eur/usd')
        btn2 = types.InlineKeyboardButton('💵USD/EUR💶', callback_data='usd/eur')
        btn3 = types.InlineKeyboardButton('💶EUR/GBP🇬🇧', callback_data='eur/gbp')
        btn4 = types.InlineKeyboardButton('❓Другая❓', callback_data='other')
        btn5 = types.InlineKeyboardButton('-->Варианты валют<--', callback_data='values')
        markup.add(btn1, btn2, btn3, btn4, btn5)  # 5 кнопок по (row_width=2)

        bot.send_message(message.chat.id, '🤗 *** ДОБРО ПОЖАЛОВАТЬ *** 🤗')
        bot.send_message(message.chat.id, '🏦ВАЛЮТНЫЙ БОТ КОНВЕРТЕР🏦')
        bot.send_message(message.chat.id, '♦️️♦️♦️️️️️️️НАШЕ МЕНЮ♦️️️♦️️♦️')
        bot.send_message(message.chat.id, '👇👇👇👇👇👇👇👇👇👇👇👇', reply_markup=markup)

        message: False  # отключаем ЭХО после вывода меню


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Итог: {round(res, 2)} \n')
        bot.register_next_step_handler(message, input_amount)  # ожидаем ввод новой суммы
    except Exception:
        bot.send_message(message.chat.id, 'Ошибка 2')
        bot.register_next_step_handler(message, my_currency)

@bot.callback_query_handler(func=lambda call: True)
# ожидание ввода USD/EUR
def callback(call):
    time.sleep(0.5)
    values = call.data.upper().split('/')
    if len(values) >= 2:
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Итог: {round(res, 2)} \n'
                                               f'Введите новую сумму')
        bot.register_next_step_handler(call.message, my_currency)

    elif call.data == 'other':
        bot.send_message(call.message.chat.id, '"валюта1/валюта2"')
        bot.register_next_step_handler(call.message, input_amount)

    elif call.data == 'values':
        bot.send_message(call.message.chat.id, 'Japan Yen 🇯🇵 :  JPY\nTurkish Lir 🇹🇳 :  TRY')

    else:
        bot.send_message(call.message.chat.id, 'Ошибка 3')
        bot.register_next_step_handler(call.message, my_currency)  # ожидание ввода USD/EUR


@bot.message_handler(func=lambda message: True)  # ожидаем любой ввод пользователя
def echo_all(message):  # слушаем любые сообщения
    bot.send_message(message.chat.id, "Для получения МЕНЮ\nНажмите кнопку --> /start")

bot.polling(none_stop=True, interval=1)  # запуск цикла работы бота