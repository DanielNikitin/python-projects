import json
import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.methods.send_message import SendMessage

router = Router()

admins = [

]
loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

items = {

}


notify = Bot(NOTIFY_TOKEN)



def test_generate(j):
    return signature.generate(j, DUMMY_SECRET)


@app.on_item_purchase()
async def my_purchase_handler(data: ItemPurchase):
    await notify.send_message(chat_id=chat_id, text=f'{data.username} купил {items[data.item_id]}')


@app.on_balance_transfer()
async def my_balance_transfer_handler(data: BalanceTransfer):
    await notify.send_message(chat_id=chat_id, text=f'{data.username} перевёл {data.amount}')


@router.message(Command("give"))
async def give(message: Message):
    if message.from_user.id not in admins:
        message.answer("???")
        return
    usr = message.text[6:]
    try:
        await message.answer(f"выдан пользователю с ником {username}")
    except Exception as e:
        await message.answer(str(e))


@router.message(Command("balance"))
async def test(message: Message):
    text = str(message.text[9:]).split(' ')
    if len(message.text) < 9:
        await message.answer("example: /balance test 1.0 1337 \n/balance username amount unique_id")
        return
    event = {
        "unique_id": text[2],
        "signature": "",
        "amount": text[1],
        "username": text[0]
    }
    await message.answer(json.dumps(event))
    result = test_generate(event)
    await message.answer(str(result))


@router.message(Command("market"))
async def test(message: Message):
    text = str(message.text[8:]).split(' ')
    if len(message.text) < 8:
        await message.answer("example: /market test 1.0 1337 wOhX6a \n/market username amount unique_id item_id")
        return
    event = {
        "item_id": text[3],
        "unique_id": text[2],
        "signature": "",
        "amount": text[1],
        "username": text[0]
    }
    await message.answer(json.dumps(event))
    result = test_generate(event)
    await message.answer(str(result))

async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
