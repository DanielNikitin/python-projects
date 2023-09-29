from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter
from app.config import CURR_API, LAT_API

import requests, json

import app.keyboard as kb

router = Router()

#                        MAIN                          #
#  **************************************************  #

@router.message(F.text == 'My ID')
async def my_id(message: Message):
    await message.answer(f'Your ID: {message.from_user.id}')
    print(f'{message.from_user.id}; {message.from_user.username}')

@router.message(F.text == 'Прочее')
async def other(message: Message):
    await message.answer('...', reply_markup=kb.other)
