from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from state_form import Form
from utils.utils import normalize_phone_number, generate_unique_code
import re


registration_router = Router()

@registration_router.message(F.chat.type == 'private', CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    user_state = await state.get_state()
    
    #! check if user is already registered. Remove comments later
    # if user_state == Form.registered:
    #     await message.answer('Вы уже зарегистрированы. Ваш профиль:')
    # else:
    await state.set_state(Form.name)
    await message.answer('Приветствую! для начала работы пройдите регистрацию.')
    await message.answer('Введите Ваше имя и фамилию.')

@registration_router.message(Form.name)
async def name_message_handler(message: Message, state: FSMContext):
    await state.set_state(Form.phone)
    await state.update_data(name=message.text)
    await message.answer('Введите Ваш номер телефона.')

@registration_router.message(Form.phone)
async def phone_message_handler(message: Message, state: FSMContext):

    phone_number_normalized = normalize_phone_number(message.text)
    if phone_number_normalized is not None:
        # check if user with given phone is already registered
        existing_user = await state.storage.get_one({'data.phone': phone_number_normalized})
        if existing_user:
            await message.answer('Пользователь с таким номером телефона уже зарегистрирован!')
        else:
            await state.set_state(Form.birth_date)
            await state.update_data(phone=phone_number_normalized)
            await message.answer('Введите Вашу дату рождения в формате ДД.ММ.ГГГГ')
    else:
        await message.answer('Некорректный формат номера телефона.') 

@registration_router.message(Form.birth_date)
async def birth_date_message_handler(message: Message, state: FSMContext):
    birth_date_pattern = re.compile(r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}$')

    if birth_date_pattern.match(message.text):
        await state.set_state(Form.registered)
        await state.update_data(birth_date=message.text)
        referal_code = generate_unique_code(8)
        await state.update_data(referal_code=referal_code)
        await message.answer(f'Вы успешно прошли регистрацию! Дарим Вам 500 приветственных бонусов!\nВаш реферальный код: {referal_code}')
    else:
        await message.answer('Некорректный формат даты.')
