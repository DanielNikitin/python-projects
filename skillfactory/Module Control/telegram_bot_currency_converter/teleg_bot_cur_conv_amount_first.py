import telebot  # выбрал его, так как уже ранее работал и мне с ним удобнее
from telebot import types  # нужен для того, чтобы обращаться напрямую без telebot.types
from currency_converter import CurrencyConverter  # https://pypi.org/project/CurrencyConverter/

bot = telebot.TeleBot('6477563848:AAHS2OiKnKFPadIl-ThW5Q0xzzfrSXmkeq0')  # API
currency = CurrencyConverter()  # подключаем в работу библиотеку конвертера
amount = 0  # первоначальное значение

@bot.message_handler(commands=['start'])  # при вводе /start, запускаем функцию start
def start(message):
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, input_amount)

def input_amount(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'i_a: Неверный формат. Введите числовое значение')
        bot.register_next_step_handler(message, input_amount)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('💶EUR/USD💵', callback_data='eur/usd')
        btn2 = types.InlineKeyboardButton('💵USD/EUR💶', callback_data='usd/eur')
        btn3 = types.InlineKeyboardButton('💶EUR/GBP🇬🇧', callback_data='eur/gbp')
        btn4 = types.InlineKeyboardButton('❓Другая❓', callback_data='other')
        btn5 = types.InlineKeyboardButton('🌐Варианты Валют🌐', callback_data='options')
        markup.add(btn1, btn2, btn3, btn4, btn5)  # 5 кнопок по (row_width=2)

        bot.send_message(message.chat.id, '🤗 *** ДОБРО ПОЖАЛОВАТЬ *** 🤗')
        bot.send_message(message.chat.id, '🏦ВАЛЮТНЫЙ БОТ КОНВЕРТЕР🏦')
        bot.send_message(message.chat.id, '♦️️♦️♦️️️️️️️НАШЕ МЕНЮ♦️️️♦️️♦️')
        bot.send_message(message.chat.id, '👇👇👇👇👇👇👇👇👇👇👇👇', reply_markup=markup)
        bot.send_message(message.chat.id, f'Вы хотите конвертировать {amount} единиц(у)')
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше "0"')
        bot.register_next_step_handler(message, input_amount)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):  # обработчик нажатых кнопок
    # так как уже ввёл значение, то
    if call.data != 'other' and call.data != 'options':  # если call.data не кнопки 'Другая' и 'Варианты Валют', то
        values = call.data.upper().split('/')  # записываем значения через '/' в переменную
        result = currency.convert(amount, values[0], values[1])  # выводим результат (значение конвертируем на value 0 и 1
        bot.send_message(call.message.chat.id, f'Result {round(result, 2)}')  # выдаём результат

    elif call.data == 'other':
        bot.send_message(call.message.chat.id, '[валюта1]/[валюта2]')
        bot.register_next_step_handler(call.message, my_currency)  # вводим желаемый тип валюты

    elif call.data == 'options':
        bot.send_message(call.message.chat.id, 'Варианты валют:')
        bot.send_message(call.message.chat.id, '1. EUR/PLN польская злота')
        bot.send_message(call.message.chat.id, '2. EUR/SEK шведская крона')
        bot.send_message(call.message.chat.id, '3. EUR/TRY турецкая лира')

def my_currency(message):  # желаемая валюта
    try:
        values = message.text.upper().split('/')  # записываем значения через '/' в переменную при помощи пользовательского ввода message text
        result = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Result {round(result, 2)}')
    except Exception:
        bot.send_message(message.chat.id, 'my_curr: Неверное значение, введите пару заново')
        bot.register_next_step_handler(message, my_currency)  # вводим желаемый тип валюты

def second_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('💶EUR/USD💵', callback_data='eur/usd')
    btn2 = types.InlineKeyboardButton('💵USD/EUR💶', callback_data='usd/eur')
    btn3 = types.InlineKeyboardButton('💶EUR/GBP🇬🇧', callback_data='eur/gbp')
    btn4 = types.InlineKeyboardButton('❓Другая❓', callback_data='other')
    btn5 = types.InlineKeyboardButton('🌐Варианты Валют🌐', callback_data='options')
    markup.add(btn1, btn2, btn3, btn4, btn5)  # 5 кнопок по (row_width=2)

    bot.send_message(message.chat.id, 'МЕНЮ', reply_markup=markup)

#--------------------------------------------------------------------------------------

@bot.message_handler(func=lambda message: True)  # ожидаем любой ввод пользователя
def text_handler(message):  # ожидаем любые сообщения
    bot.send_message(message.chat.id, "Для получения МЕНЮ\nНажмите кнопку --> /start")

bot.polling(none_stop=True)  # бесперебойная работа бота
