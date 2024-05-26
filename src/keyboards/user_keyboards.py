from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def user_keyboard():
    kb = [
        [KeyboardButton(text='Мой аккаунт')],
        [KeyboardButton(text='Бонусы')],
        [KeyboardButton(text='Обратная связь')],
    ]

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
    return keyboard

