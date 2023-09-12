import telebot
from currency_converter import CurrencyConverter  # https://pypi.org/project/CurrencyConverter/
from telebot import types

bot = telebot.TeleBot('6477563848:AAHS2OiKnKFPadIl-ThW5Q0xzzfrSXmkeq0')
currency = CurrencyConverter()
amount = 1

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('💶EUR/USD💵', callback_data='eur/usd')
    btn2 = types.InlineKeyboardButton('💵USD/EUR💶', callback_data='usd/eur')
    btn3 = types.InlineKeyboardButton('EUR/GBP🇬🇧', callback_data='eur/gbp')
    btn4 = types.InlineKeyboardButton('❓Другая валюта❓', callback_data='else')
    btn5 = types.InlineKeyboardButton('-->Варианты валют<--', callback_data='values')
    btn6 = types.InlineKeyboardButton('Калькулятор валюты', callback_data='another_button')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    markup.add(btn6)

    bot.send_message(message.chat.id, '🤗 *** ДОБРО ПОЖАЛОВАТЬ *** 🤗')
    bot.send_message(message.chat.id, '🏦-ВАЛЮТНЫЙ БОТ КОНВЕРТЕР-🏦')
    bot.send_message(message.chat.id, '🏦-ВАЛЮТНЫЙ БОТ КОНВЕРТЕР-🏦')
    bot.send_message(message.chat.id, '♦️ОЗНАКОМЬТЕСЬ С НАШИМ МЕНЮ♦️')
    bot.send_message(message.chat.id, '👇👇👇👇👇👇👇👇👇👇👇👇', reply_markup=markup)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный ввод')
        bot.register_next_step_handler(message, summa)
        return

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    values = call.data.upper().split('/')
    if len(values) >= 2:
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Итог: {round(res, 2)}. \nВведите новую сумму.')
        bot.register_next_step_handler(call.message, summa)
    elif call.data == 'else':
        bot.send_message(call.message.chat.id, 'ПРИМЕР ВВОДА: [** eur/gbp **]\nПРИМЕРЫ ДОСТУПНЫ В -->"ВАРИАНТЫ ВАЛЮТЫ"')
        bot.register_next_step_handler(call.message, my_currency)
    elif call.data == 'values':
        bot.send_message(call.message.chat.id, 'Japan Yen 🇯🇵 :  JPY,\nTurkish Lir 🇹🇳 :  TRY')
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