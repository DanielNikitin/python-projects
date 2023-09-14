import telebot
from config import bot
from extensions import CurrencyBot

if __name__ == '__main__':
    currency_bot = CurrencyBot(bot)
    currency_bot.run()
    bot.polling(none_stop=True)