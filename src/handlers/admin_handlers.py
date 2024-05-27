from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from state_form import Form
from keyboards.admin_keyboards import bonus_keyboard, admin_keyboard, back_keyboard, mailing_keyboard
from utils.utils import mail
admin_router = Router()





@admin_router.message(Form.admin_authorized, F.text.casefold() == 'изменение баланса пользователя')
async def bonus_handler(message: Message, state: FSMContext):
    await message.answer('Введите реферальный код пользователя', reply_markup=back_keyboard())
    await state.set_state(Form.admin_referal_code)


@admin_router.message(Form.admin_referal_code)
async def referal_code_handler(message: Message, state: FSMContext):
    user = await state.storage.get_one({'data.referal_code': message.text})
    if user is None:
        await message.answer('Пользователя с таким кодом не существует')
    else:
        await state.set_state(Form.admin_bonus_points)
        await state.update_data(user_referal_code=message.text)
        user_data = user.get('data')
        await message.answer(f"Пользователь\nФИ: {user_data.get('name')}\nНомер телефона: {user_data.get('phone')}\nДата рождения: {user_data.get('birth_date')}\nБонусы: {user_data.get('bonus_points')}\nРеферальный код: {user_data.get('referal_code')}", reply_markup=bonus_keyboard())


@admin_router.message(Form.admin_bonus_points, F.text.casefold() == 'списать')
async def bonus_sub_choice_handler(message: Message, state: FSMContext):

    await state.set_state(Form.admin_bonus_point_sub)
    await message.answer('Введите количество бонусов для списания', reply_markup=back_keyboard())
 
        
@admin_router.message(Form.admin_bonus_points, F.text.casefold() == 'начислить')
async def bonus_add_choice_handler(message: Message, state: FSMContext):
    await state.set_state(Form.admin_bonus_points_add)
    await message.answer('Введите количество бонусов для начисления', reply_markup=back_keyboard())


@admin_router.message(Form.admin_bonus_point_sub, F.text.isdigit())
async def bonus_sub_handler(message: Message, state: FSMContext):
    points = int(message.text)
    if points < 0:
        await message.answer('Некорректное число бонусов')
    else:
        data = await state.get_data()
        referal_code = data.get('user_referal_code')
        user = await state.storage.get_one({'data.referal_code': referal_code})
        user_data = user.get('data')
        user_points = user_data.get('bonus_points')
        if points > user_points:
            await message.answer('У пользователя не может быть отрицательное число бонусов')
        else:
            total_points = user_points - points
            await state.storage.update_certain_data({'data.referal_code': referal_code}, {'bonus_points': total_points})
            await message.answer(f'Бонусы списаны. Текущий баланс пользователя: {total_points}', reply_markup=admin_keyboard())
            await mail([user], f'У Вас списано {points} бонусов')
            await state.set_state(Form.admin_authorized)


    
@admin_router.message(Form.admin_bonus_points_add, F.text.isdigit())
async def bonus_add_handler(message: Message, state: FSMContext):
    points = int(message.text)
    if points < 0:
        await message.answer('Некорректное число бонусов')
    else:
        data = await state.get_data()
        referal_code = data.get('user_referal_code')
        user = await state.storage.get_one({'data.referal_code': referal_code})
        user_data = user.get('data')
        user_points = user_data.get('bonus_points')
        total_points = user_points + points
        await state.storage.update_certain_data({'data.referal_code': referal_code}, {'bonus_points': total_points})
        await message.answer(f'Бонусы начислены. Текущий баланс пользователя: {total_points}', reply_markup=admin_keyboard())
        await mail([user], f'Вам начислено {points} бонусов')
        await state.set_state(Form.admin_authorized)




@admin_router.message(Form.admin_authorized, F.text.casefold() == 'рассылки')
async def mailing_handler(message: Message, state: FSMContext):
    await message.answer('Выберите вариант рассылки', reply_markup=mailing_keyboard())
    await state.set_state(Form.admin_message_send)

@admin_router.message(Form.admin_message_send, F.text.casefold() == 'всем пользователям')
async def all_user_mail_handler(message: Message, state: FSMContext):
    await message.answer('Введите сообщение для отправки', reply_markup=back_keyboard())
    await state.set_state(Form.admin_message_text)

@admin_router.message(Form.admin_message_send, F.text.casefold() == 'выбранному пользователю')
async def one_user_mail_handler(message: Message, state: FSMContext):
    await message.answer('Введите реферальный код пользователя', reply_markup=back_keyboard())
    await state.set_state(Form.admin_message_send_one)

@admin_router.message(Form.admin_message_send_one)
async def one_user_code_handler(message: Message, state: FSMContext):
    user = await state.storage.get_one({'data.referal_code': message.text})
    if user is None:
        await message.answer('Пользователя с таким кодом не существует')
    else:
        await state.update_data(user_referal_code=message.text)
        await message.answer('Введите сообщение для отправки')
        await state.set_state(Form.admin_message_text_one)

@admin_router.message(Form.admin_message_text)
async def message_text_handler(message: Message, state: FSMContext):
    users = await state.storage.get_all_data({})
    print(users)
    await mail(users, message.text)
    await message.answer('Сообщения отправлены', reply_markup=admin_keyboard())
    await state.set_state(Form.admin_authorized)


@admin_router.message(Form.admin_message_text_one)
async def message_text_one_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    user = await state.storage.get_one({'data.referal_code':data.get('user_referal_code')})
    print(user)
    await mail([user], message.text)
    await message.answer('Сообщение отправлено', reply_markup=admin_keyboard())
    await state.set_state(Form.admin_authorized)

