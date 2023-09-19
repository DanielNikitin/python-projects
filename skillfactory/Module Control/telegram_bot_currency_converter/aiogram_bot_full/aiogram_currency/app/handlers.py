from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter
import requests, json
from config import curr_api

import app.keyboards as kb

# Рутер это 'поисковик' среди директорий
router = Router()

@router.message(F.text == '/start')
async def start(message: Message):
    await message.answer('Welcome to the DCG Bot!', reply_markup=kb.main)

@router.message(F.text == 'Contacts')
async def contacts(message: Message):
    await message.answer('Our contacts:', reply_markup=kb.socials)

@router.message(F.text == 'Catalogue')
async def catalog(message: Message):
    await message.answer('Choose a category', reply_markup=kb.catalog)


# Хэндлер без фильтра, сработает, если ни один выше не сработает.
@router.message()
async def echo(message: Message):
    await message.answer('Press to -> /start')