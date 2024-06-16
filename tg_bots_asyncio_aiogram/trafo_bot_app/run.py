import asyncio
from aiogram import Bot, Dispatcher

from app.main_handler import router
from app.root_handler import root_router
from app.converter_handler import conv_router
from app.maint_handler import maint_router

from app.start_handler import start_router

from app.config import BOT_API, TEST_API

from app.main_handler import set_bot  # вызываем функцию для привязки переменной

# Polling, т.е бесконечный цикл проверки апдейтов
async def main():
    bot = Bot(token=BOT_API)
    dp = Dispatcher()

    set_bot(bot)  # передаем значение (bot) для функции set_bot

    dp.include_router(router)
    dp.include_router(root_router)
    dp.include_router(conv_router)
    dp.include_router(maint_router)
    dp.include_router(start_router)

    await dp.start_polling(bot)


# Функция main() запускается только в случае если скрипт запущен с этого файла
if __name__ == '__main__':
    try:
        print("BOT STARTED")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')