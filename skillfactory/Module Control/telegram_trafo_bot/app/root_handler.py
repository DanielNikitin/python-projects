from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Filter

import app.keyboard as kb

root_router = Router()

# Список Root Group
root_id = [1035107072, # Daniel
            103200201  # Dima
          ]

#                        ROOT                          #
#  **************************************************  #

class Root(Filter):
    # фильтр проверяет сообщения в чате
    async def __call__(self, message: Message) -> bool:
        # если сообщение от root_id то возвращает True
        return message.from_user.id in root_id

@root_router.message(Root(), F.text == 'Root')
async def maintenance_status(message: Message):
    await message.answer('Root Status OK', reply_markup=kb.root)

@root_router.message(F.text == 'Database Menu')
async def database(message: Message):
    await message.answer("...", reply_markup=kb.database_menu)

@root_router.message(F.text == 'Database')
async def database(message: Message):
    await message.answer("...", reply_markup=kb.database)

@root_router.message(F.text == 'Table')
async def database(message: Message):
    await message.answer("...", reply_markup=kb.table)

@root_router.message(F.text == 'Parts')
async def database(message: Message):
    await message.answer("...", reply_markup=kb.parts)

@root_router.message(F.text == 'Back')
async def database(message: Message):
    await message.answer("...", reply_markup=kb.main)