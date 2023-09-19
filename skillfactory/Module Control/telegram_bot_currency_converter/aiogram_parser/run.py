import asyncio
import requests, json
from config import token
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter

# Рутер это 'поисковик' среди директорий
router = Router()


@router.message(F.text == '/start')
async def start(message: Message):
    await message.answer('Добро пожаловать!')

# Хэндлер без фильтра, сработает, если ни один выше не сработает.
@router.message()
async def echo(message: Message):
    await message.answer('Нажми на -> /start')
    await message.answer('Нажми на -> /my_id')


# Polling, т.е бесконечный цикл проверки апдейтов
async def main():
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


# Функция main() запускается только в случае если скрипт запущен с этого файла
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')