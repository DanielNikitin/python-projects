











@router.message(F.text == 'Другой Вариант')
async def start_custom_input(message: Message):
    # Устанавливаем состояние пользователя в ожидание ввода
    user_states[message.chat.id] = "waiting_for_input"
    await message.reply("Введите текст, который вы хотите записать в переменную:")

@router.message(lambda message: user_states.get(message.chat.id) == "waiting_for_input")
async def handle_custom_input(message: Message):
    user_state = user_states.get(message.chat.id)
    if user_state == "waiting_for_input":
        text_value = message.text
        chat_data[message.chat.id] = text_value
        user_states[message.chat.id] = None  # Сбрасываем состояние пользователя
        await message.reply(f"Сообщение записано в переменную: {text_value}")