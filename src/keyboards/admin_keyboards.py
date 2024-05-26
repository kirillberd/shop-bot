from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def admin_keyboard():
    kb = [
        [KeyboardButton(text='Изменения баланса пользователя')],
        [KeyboardButton(text='Рассылки')],
    ]

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
    return keyboard

