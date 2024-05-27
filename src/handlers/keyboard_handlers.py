from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from state_form import Form
from aiogram.filters import Command
from os import getenv
from dotenv import load_dotenv
from keyboards.admin_keyboards import admin_keyboard, back_keyboard
from keyboards.user_keyboards import user_keyboard
load_dotenv()

keyboard_router = Router()



@keyboard_router.message(Form.registered, F.text.casefold() == 'мой аккаунт')
async def account_details_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(f"Ваш профиль\nФИ: {user_data.get('name')}\nНомер телефона: {user_data.get('phone')}\nДата рождения: {user_data.get('birth_date')}")


@keyboard_router.message(Form.registered, F.text.casefold() == 'бонусы')
async def referal_details_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(f"Реферальная программа\nВаши бонусы: {user_data.get('bonus_points')}\nВаш реферальный код: {user_data.get('referal_code')}")

@keyboard_router.message(Form.registered, F.text.casefold() == 'обратная связь')
async def support_handler(message: Message, state: FSMContext):
    await message.answer(f'По интересующим вопросам свяжитесь с нами в: тут будут ссылки.')
    

@keyboard_router.message(Form.registered, Command('admin'))
async def admin_command_handler(message: Message, state: FSMContext):
    await state.set_state(Form.admin_start_registered)
    await message.answer('Для авторизации в качестве администратора введите пароль', reply_markup=back_keyboard())

@keyboard_router.message(Form.admin_start_registered)
async def admin_start_handler(message: Message, state: FSMContext):
    if message.text.casefold() == 'назад':
        await state.set_state(Form.registered)
        await message.answer('Главное меню', reply_markup=user_keyboard())

    elif message.text == getenv('ADMIN_PASSWORD'):
        await state.update_data(role='admin')
        await state.set_state(Form.admin_authorized)
        await message.answer('Авторизация прошла успешна, вам доступна панель администратора', reply_markup=admin_keyboard())
    else:
        await message.answer('Неверный пароль.')


