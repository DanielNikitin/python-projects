from telebot import types
from currency_converter import CurrencyConverter

class Menu:
    @staticmethod
    def main_markup():
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('💶EUR/USD💵', callback_data='eur/usd')
        btn2 = types.InlineKeyboardButton('💵USD/EUR💶', callback_data='usd/eur')
        btn3 = types.InlineKeyboardButton('💶EUR/GBP🇬🇧', callback_data='eur/gbp')
        btn4 = types.InlineKeyboardButton('❓Другая❓', callback_data='other')
        btn5 = types.InlineKeyboardButton('🌐Варианты Валют🌐', callback_data='options')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        return markup

    @staticmethod
    def other_markup():
        # Создайте другие меню, если необходимо
        pass

class CurrencyBot:
    def __init__(self, bot):
        self.bot = bot
        self.currency = CurrencyConverter()
        self.amount = 0

    def main_menu(self, message):
        markup = Menu.main_markup()
        self.bot.send_message(message.chat.id, '🤗 *** ДОБРО ПОЖАЛОВАТЬ *** 🤗')
        self.bot.send_message(message.chat.id, '🏦ВАЛЮТНЫЙ БОТ КОНВЕРТЕР🏦')
        self.bot.send_message(message.chat.id, '♦️️♦️♦️️️️️️️НАШЕ МЕНЮ♦️️️♦️️♦️')
        self.bot.send_message(message.chat.id, '👇👇👇👇👇👇👇👇👇👇', reply_markup=markup)
        self.bot.send_message(message.chat.id, 'Какое количество единиц вы хотите конвертировать?\n'
                                              'Введите нужное вам значение...')
        self.bot.register_next_step_handler(message, self.input_amount)

    def input_amount(self, message):
        try:
            self.amount = int(message.text.strip())
            self.bot.send_message(message.chat.id, 'Теперь выберите кнопку из меню')
        except ValueError:
            self.bot.send_message(message.chat.id, 'i_a: Неверный формат. Введите числовое значение')
            self.bot.register_next_step_handler(message, self.input_amount)
            return

    def my_currency(self, message):
        try:
            values = message.text.upper().split('/')
            result = self.currency.convert(self.amount, values[0], values[1])
            self.bot.send_message(message.chat.id, f'{values} = {round(result, 2)}')
        except Exception:
            self.bot.send_message(message.chat.id, 'my_curr: Неверное значение, введите пару заново')
            self.bot.register_next_step_handler(message, self.my_currency)

    def send_menu_message(self, chat_id):
        markup = Menu.main_markup()
        self.bot.send_message(chat_id, 'МЕНЮ', reply_markup=markup)

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.main_menu(message)

        @self.bot.message_handler(func=lambda message: True)
        def text_handler(message):
            self.send_menu_message(message.chat.id)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback(call):
            if call.data != 'other' and call.data != 'options':
                values = call.data.upper().split('/')
                result = self.currency.convert(self.amount, values[0], values[1])
                self.bot.send_message(call.message.chat.id, f'Result {round(result, 2)}')
            elif call.data == 'other':
                self.bot.send_message(call.message.chat.id, '[валюта1]/[валюта2]')
                self.bot.register_next_step_handler(call.message, self.my_currency)
            elif call.data == 'options':
                self.bot.send_message(call.message.chat.id, 'Возможные Варианты:')
                self.bot.send_message(call.message.chat.id, '1. EUR/PLN польская злота\n'
                                                           '2. EUR/SEK шведская крона\n'
                                                           '3. EUR/TRY турецкая лира\n'
                                                           '4. RUB/TRY рубли в турецкие лиры')
