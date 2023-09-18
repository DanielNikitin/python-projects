from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter

import app.keyboards as kb

# Рутер это 'поисковик' среди директорий
router = Router()

class Admin(Filter):  # дочерний класс Admin у Родителя Filter
    async def __call__(self, message: Message):
        return message.from_user.id in [1035107072]

@router.message(Admin(), F.text == '/admin')
async def admin(message: Message):
    await message.answer('yies')

@router.message(F.text == '/start')
async def start(message: Message):
    await message.answer('Добро пожаловать!', reply_markup=kb.main)

# Получение id/имени с помощью message.from_user.id
@router.message(F.text == '/my_id')
async def my_id(message: Message):
    await message.answer(f'Ваш ID: {message.from_user.id}')
    await message.reply(f'Ваше имя: {message.from_user.first_name}')
    await message.answer_photo(photo='https://cs13.pikabu.ru/post_img/2022/12/14/6/1671008037224421279.jpg',
                                caption='Это пример отправки мемов')
    print(message)

@router.message(F.text == 'Контакты')
async def contacts(message: Message):
    await message.answer('Наши контакты:', reply_markup=kb.socials)

@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию', reply_markup=kb.catalog)

@router.callback_query(F.data == 'Garrett')
async def cb_catalogue(callback: CallbackQuery):
    #await callback.answer("Вы выбрали бренд")  # полупрозрачная табличка
    await callback.answer("Вы выбрали бренд", show_alert=True)  # отдельное окно
    await callback.message.answer(f'...Вы выбрали {callback.data}...')  # сообщение в чат



# Хэндлер без фильтра, сработает, если ни один выше не сработает.
@router.message()
async def echo(message: Message):
    await message.answer('Нажми на -> /start')
    await message.answer('Нажми на -> /my_id')
