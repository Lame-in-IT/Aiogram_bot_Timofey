from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Каталог'
        ),
        KeyboardButton(
            text='Корзина'
        ),
        KeyboardButton(
            text='FAQ'
        )
    ]
], resize_keyboard=True)