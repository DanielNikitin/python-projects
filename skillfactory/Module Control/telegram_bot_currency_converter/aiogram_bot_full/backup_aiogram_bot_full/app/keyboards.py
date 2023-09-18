from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)

main_kb = [
    [KeyboardButton(text='Каталог'),
     KeyboardButton(text='Корзина')],
    [KeyboardButton(text='Мой профиль'),
     KeyboardButton(text='Контакты')]
          ]


main = ReplyKeyboardMarkup(keyboard=main_kb,
                           resize_keyboard=True,
                           input_field_placeholder='усатый петушитель')


socials = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Telegram', url='https://t.me/dcg_tallinn')],
    [InlineKeyboardButton(text='Instagram', url='https://www.google.ru/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwipqY7AiLWBAxUkJxAIHS5qCnkQFnoECA4QAQ&url=https%3A%2F%2Fwww.instagram.com%2Fdcg_tallinn%2F&usg=AOvVaw3O1cMUQggg4eM6ajiEMDwG&opi=89978449')]
                                                ])

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Garrett', callback_data='Garrett')],
    [InlineKeyboardButton(text='BorgWarner', callback_data='BorgWarner')]
                                                ])