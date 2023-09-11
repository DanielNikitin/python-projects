import telebot
from currency_converter import CurrencyConverter  # https://pypi.org/project/CurrencyConverter/
from telebot import types

bot = telebot.TeleBot('6477563848:AAHS2OiKnKFPadIl-ThW5Q0xzzfrSXmkeq0')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный ввод')
        bot.register_next_step_handler(message, summa)
        return

    if amount >0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn2 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn3 = types.InlineKeyboardButton('EUR/RUB', callback_data='eur/rub')
        btn4 = types.InlineKeyboardButton('Другая валюта', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Итог: {round(res, 2)}. \nМожете отправить запрос заново.')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару через "/",\nнапр. eur/gbp')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Итог: {round(res, 2)}. \nМожете отправить запрос заново.')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'My_Curr: Что-то не так')
        bot.register_next_step_handler(message, my_currency)

bot.polling(none_stop=True)