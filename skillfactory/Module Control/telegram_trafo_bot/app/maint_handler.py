from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Filter

import app.keyboard as kb

maint_router = Router()

# Список Maintenance Group
maintenance_id = [1035107072, # Daniel
                  103200201   # Dima
                 ]

class Maintenance(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in maintenance_id

@maint_router.message(Maintenance(), F.text == 'Maintenance')
async def maintenance_status(message: Message):
    await message.answer('Maintenance Status OK', reply_markup=kb.maintenance)

@maint_router.message(F.text == 'Jig Calibration')
async def jig_calib(message: Message):
    await message.answer("...", reply_markup=kb.jig)

# --------

@maint_router.message(F.text == 'Ввести модель JIG')
async def jig_number(message: Message):
    await message.answer("Ввести номер JIG")

@maint_router.message(F.text == 'Список рабочих мест')
async def list_places(message: Message):
    await message.answer("Список рабочих мест")

@maint_router.message(F.text == 'Список JIG')
async def jig_list(message: Message):
    await message.answer("Список JIG")

@maint_router.message(F.text == 'Чертежи')
async def jig_blueprint(message: Message):
    await message.answer("Чертежи")

@maint_router.message(F.text == 'Back')
async def database(message: Message):
    await message.answer("...", reply_markup=kb.main)