import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.config import bot_token


# Polling, т.е бесконечный цикл проверки апдейтов
async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


# Функция main() запускается только в случае если скрипт запущен с этого файла
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')