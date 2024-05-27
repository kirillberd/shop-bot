from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def admin_keyboard():
    kb = [
        [KeyboardButton(text='Изменение баланса пользователя')],
        [KeyboardButton(text='Рассылки')],
    ]

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
    return keyboard

def bonus_keyboard():
    kb = [
        [KeyboardButton(text='Списать')],
        [KeyboardButton(text='Начислить')],
        [KeyboardButton(text='Назад')],
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
    return keyboard
def back_keyboard():
    kb = [
        [KeyboardButton(text='Назад')]

    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)

    return keyboard

def mailing_keyboard():
    kb = [
        [KeyboardButton(text='Всем пользователям')],
        [KeyboardButton(text='Выбранному пользователю')],
        [KeyboardButton(text='Назад')],
    ]

    keyborad = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
    return keyborad

