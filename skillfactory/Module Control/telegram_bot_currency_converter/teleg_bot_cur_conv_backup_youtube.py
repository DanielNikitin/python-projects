import telebot
from telebot import types
from currency_converter import CurrencyConverter

bot = telebot.TeleBot('6477563848:AAHS2OiKnKFPadIl-ThW5Q0xzzfrSXmkeq0')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, input_amount)

def input_amount(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите числовое значение')
        bot.register_next_step_handler(message, input_amount)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('💶EUR/USD💵', callback_data='eur/usd')
        btn2 = types.InlineKeyboardButton('💵USD/EUR💶', callback_data='usd/eur')
        btn3 = types.InlineKeyboardButton('💶EUR/GBP🇬🇧', callback_data='eur/gbp')
        btn4 = types.InlineKeyboardButton('❓Другая❓', callback_data='other')
        markup.add(btn1, btn2, btn3, btn4)

        bot.send_message(message.chat.id, '🤗 *** ДОБРО ПОЖАЛОВАТЬ *** 🤗')
        bot.send_message(message.chat.id, '🏦ВАЛЮТНЫЙ БОТ КОНВЕРТЕР🏦')
        bot.send_message(message.chat.id, '♦️️♦️♦️️️️️️️НАШЕ МЕНЮ♦️️️♦️️♦️')
        bot.send_message(message.chat.id, '👇👇👇👇👇👇👇👇👇👇👇👇', reply_markup=markup)
        bot.send_message(message.chat.id, f'Вы хотите конвертировать {amount} единиц')
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше "0"')
        bot.register_next_step_handler(message, input_amount)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'other':
        values = call.data.upper().split('/')
        result = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Result {round(result, 2)}')
    else:
        bot.send_message(call.message.chat.id, '[валюта1]/[валюта2]')
        bot.send_message(call.message.chat.id, 'Введите пару валют (например, USD/EUR):')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        result = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Result {round(result, 2)}')
    except Exception:
        bot.send_message(message.chat.id, 'Неверное значение, введите пару заново')

bot.polling(none_stop=True)
