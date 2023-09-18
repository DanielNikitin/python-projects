import telebot
from config import bot
from extensions import CurrencyBot

if __name__ == '__main__':
    bot.polling(none_stop=True)