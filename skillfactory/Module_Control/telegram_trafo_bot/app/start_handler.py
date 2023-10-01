from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Filter

from app.keyboard import root_keyboard

import app.keyboard as kb


start_router = Router()

# Список Root Group
root_id = [1035107072,  # Daniel
           103200201    # Dima
          ]

# Список Maintenance Group
maintenance_id = [1035107072, # Daniel
                  103200201   # Dima
                 ]

@start_router.message(F.text == '/start')
async def start(message: Message):
    user_id = message.from_user.id
    main_kb = root_keyboard(user_id, root_id, maintenance_id)


    await message.answer('Welcome to the DCG Multi Bot!', reply_markup=main_kb)
    await message.answer('Нажмите на любую кнопку из Меню')
    await message.answer('http://dcg.ee')
    print(f'{message.from_user.id} main menu')

@start_router.message()
async def welcome(message: Message):
    await message.answer('Dont type, just Press -> /start')