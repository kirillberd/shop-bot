from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from state_form import Form


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
    