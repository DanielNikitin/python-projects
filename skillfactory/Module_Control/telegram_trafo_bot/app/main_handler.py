from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Filter
from app.config import CURR_API, LAT_API

import requests, json

import app.keyboard as kb

router = Router()


#                        MAIN                          #
#  **************************************************  #

def set_bot(bot):  # ловим параметр bot из run.py
    router.bot = bot  # прикручиваем его к router.bot чтобы не вызывать конфликт

@router.message(F.text == 'My ID')
async def my_id(message: Message):
    await message.answer(f'Your ID: {message.from_user.id}')
    print(f'{message.from_user.id}; {message.from_user.username}')

@router.message(F.text == 'Прочее')
async def other(message: Message):
    await message.answer('...', reply_markup=kb.other)

@router.message(F.text == 'Обновления')
async def updates(message: Message):

    audio = FSInputFile(path=r'/tg_bot/dcg_bot/audio/test.mp3')
    await router.bot.send_audio(message.chat.id, audio=audio)

    message_text2 = (
        '** 31.09 FUTURE TIME **\n'
        '👉🏻 Тестировочные Усы вперёд за работу, кек\n'
        '👉🏻 чувак это репчик'
    )
    await message.answer(message_text2)

    message_text1 = (
        '** 30.09 04:30 **\n'
        '👉🏻 При нажатии на Database Menu происходит подключение к Database.\n'
        '👉🏻 Если соединение успешно, то вывод дальнейшего меню, если нет, то ошибка.\n'
        '👉🏻 Внутри Database подключил кнопку Add для добавления баз данных.\n'
        '👉🏻 Внутри Database подключил кнопку Remove для удаления базы данных.\n'
        '👉🏻 Внутри Database подключил кнопку List для вывода списка баз данных.\n'
        '👉🏻 Выполнены проверки на Наличие БД и соответствующий вывод.\n'
        '👉🏻 Добавлены логи для отслеживания действий внутри Root.\n'
        '👉🏻 Бот запущен на VPS\n'
        '👉🏻 Добавил отправку голосового сообщения через бота'
    )
    await message.answer(message_text1)

# https://www.youtube.com/watch?v=0n1120vZbpk

# https://codeby.net/forums/powershell-python.136/