from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)

main_kb = [
    [KeyboardButton(text='Catalogue'),
     KeyboardButton(text='My profile')],
    [KeyboardButton(text='Meme'),
     KeyboardButton(text='Contacts')]
          ]


main = ReplyKeyboardMarkup(keyboard=main_kb,
                           resize_keyboard=True,
                           input_field_placeholder='daily customs garage')


socials = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Telegram', url='https://t.me/dcg_tallinn')],
    [InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/dcg_tallinn/')]
                                                ])

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Garrett', callback_data='Garrett')],
    [InlineKeyboardButton(text='BorgWarner', callback_data='BorgWarner')]
                                                ])