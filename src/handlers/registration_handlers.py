from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from ..state_form import Form
import re


registration_router = Router()

@registration_router.message(F.chat.type == 'private', CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    message.answer('Приветствую! для начала работы пройдите регистрацию.')
    message.answer('Введите Ваше имя и фамилию.')

@registration_router.message(Form.name)
async def name_message_handler(message: Message, state: FSMContext):
    await state.set_state(Form.phone)
    await state.update_data(name=message.text)
    await message.answer('Введите Ваш номер телефона.')

@registration_router.message(Form.phone)
async def phone_message_handler(message: Message, state: FSMContext):
    phone_pattern = re.compile(r'^(?:\+7|8)?[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$')

    if phone_pattern.match(message.text):
        await state.set_state(Form.birth_date)
        await state.update_data(phone=message.text)
        await message.answer('Введите Вашу дату рождения в формате ДД.ММ.ГГГГ')
    else:
        await message.answer('Некорректный формат номера телефона.')

@registration_router.message(Form.birth_date)
async def birth_date_message_handler(message: Message, state: FSMContext):
    birth_date_pattern = pattern = re.compile(r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}$')

    if birth_date_pattern.match(message.text):
        await state.set_state(Form.registered)
        await state.update_data(birth_date=message.text)
        await message.answer('Вы успешно прошли регистрацию! Дарим Вам 500 приветственных бонусов!')
    else:
        await message.answer('Некорректный формат даты.')
