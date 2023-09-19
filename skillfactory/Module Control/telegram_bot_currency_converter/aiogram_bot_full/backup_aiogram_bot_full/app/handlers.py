from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter
import requests, json

import app.keyboards as kb

# Рутер это 'поисковик' среди директорий
router = Router()

class Admin(Filter):  # дочерний класс Admin у Родителя Filter
    async def __call__(self, message: Message):
        return message.from_user.id in [1035107072, 1057410060]

@router.message(Admin(), F.text == '/admin')
async def admin(message: Message):
    await message.answer('yies')

@router.message(F.text == '/start')
async def start(message: Message):
    await message.answer('Welcome to the DCG Bot!', reply_markup=kb.main)

# Получение id/имени с помощью message.from_user.id
@router.message(F.text == 'My profile')
async def my_id(message: Message):
    await message.answer(f'Your ID: {message.from_user.id}')
    await message.reply(f'Your Name: {message.from_user.first_name}')
    print(message)

@router.message(F.text == 'Contacts')
async def contacts(message: Message):
    await message.answer('Our contacts:', reply_markup=kb.socials)

@router.message(F.text == 'Meme')
async def catalog(message: Message):
    await message.answer('Picture example')
    await message.answer_photo(photo='https://cs13.pikabu.ru/post_img/2022/12/14/6/1671008037224421279.jpg',
                                caption='Это пример отправки мемов')

@router.message(F.text == 'Catalogue')
async def catalog(message: Message):
    await message.answer('Choose a category', reply_markup=kb.catalog)

@router.callback_query(F.data == 'Garrett')
async def cb_catalogue(callback: CallbackQuery):
    await callback.answer("Вы выбрали бренд")  # полупрозрачная табличка
    await callback.message.answer(f'...Вы выбрали {callback.data}...')  # сообщение в чат

@router.callback_query(F.data == 'BorgWarner')
async def cb_catalogue(callback: CallbackQuery):
    await callback.answer("Вы выбрали бренд", show_alert=True)  # отдельное окно
    await callback.message.answer(f'...Вы выбрали {callback.data}...')  # сообщение в чат


# Хэндлер без фильтра, сработает, если ни один выше не сработает.
@router.message()
async def echo(message: Message):
    await message.answer('Press to -> /start')