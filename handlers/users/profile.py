from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from filters.users_filters import IsNotClientCallback
from keyboards.inline.callback_datas import metro_data, local_object_data
from keyboards.inline.inline_keyboards import generate_keyboard_with_metro_profile, get_available_local_objects_profile
from loader import dp, db
from states.profile_states import ProfileState
from utils.emoji import warning_em


@dp.callback_query_handler(text='cancel', state=[ProfileState.WaitMetro,
                                                 ProfileState.WaitLocation,
                                                 ProfileState.WaitAddress])
async def send_categories_menu(call: CallbackQuery, state: FSMContext):
    """Отправляем информацию профиля"""
    await call.message.edit_reply_markup()
    user_info = await db.get_user_profile_info(call.from_user.id)
    if user_info['user_address']:
        await call.message.answer(f"Ваш профиль\n"
                                  f"\n"
                                  f"User ID: {user_info['user_telegram_id']}\n"
                                  f"Адрес доставки: {user_info['local_object_name']}\n"
                                  f"Параметры доставки: {user_info['user_address']}",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text='Изменить',
                                              callback_data='change_profile'
                                          )
                                      ]
                                  ]))
    else:
        await call.message.answer(text=f"Ваш профиль\n"
                                       f"\n"
                                       f"User ID: {user_info['user_telegram_id']}\n"
                                       f"Адрес доставки: {user_info['local_object_name']}\n"
                                       f"{warning_em} Параметры доставки: Не указаны",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text='Изменить',
                                              callback_data='change_profile'
                                          )
                                      ]
                                  ]))
    await state.finish()


@dp.callback_query_handler(text='change_profile')
async def change_profile(call: CallbackQuery):
    """Пользователь нажимает изменить"""
    await call.message.edit_reply_markup()
    await call.message.answer(f"Для начала выберите ближайшую станцию метро.",
                              reply_markup=await generate_keyboard_with_metro_profile())
    await ProfileState.WaitMetro.set()


@dp.callback_query_handler(metro_data.filter(), state=ProfileState.WaitMetro)
async def get_user_location(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Предлагаем пользователю выбрать локацию"""
    await call.message.edit_reply_markup()
    await call.answer(cache_time=10)
    metro_id = int(callback_data.get('metro_id'))
    await state.update_data(metro_id=metro_id)
    metro_name = await db.get_metro_name_by_metro_id(metro_id)
    await call.message.answer(f"Вы выбрали {metro_name} \n"
                              f"Выберите объект локальной доставки",
                              reply_markup=await get_available_local_objects_profile(metro_id))
    await ProfileState.WaitLocation.set()


@dp.callback_query_handler(local_object_data.filter(), state=ProfileState.WaitLocation)
async def get_user_address(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Просим ввести адрес пользователя"""
    await call.message.edit_reply_markup()
    local_object_id = int(callback_data.get('local_object_id'))
    await state.update_data(local_object_id=local_object_id)
    await call.message.answer(f'Напишите точное место доставки и номер телефона для связи.\n'
                              f'Пример 1: Подъезд 2, 15 этаж, офис 123, ООО Компания, ФИО покупателя, 89160000000\n'
                              f'Пример 2: Северный вход, у ресепшн, 89160000000',
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [
                                      InlineKeyboardButton(
                                          text="Введу адрес позже",
                                          callback_data='address_later'
                                      )
                                  ],
                                  [
                                      InlineKeyboardButton(
                                          text='Отмена',
                                          callback_data='cancel'
                                      )
                                  ]
                              ]))
    await ProfileState.WaitAddress.set()


@dp.callback_query_handler(IsNotClientCallback(), text='address_later', state=ProfileState.WaitAddress)
async def set_change_profile_without_address(call: CallbackQuery, state: FSMContext):
    """Обновляем данные профиля без адреса"""
    data = await state.get_data()
    local_object_id = data.get('local_object_id')
    loc_data = await db.get_local_object_data_by_id(local_object_id)
    await db.add_user(call.from_user.id,
                      loc_data['local_object_metro_id'],
                      loc_data['local_object_location_id'],
                      local_object_id
                      )
    await call.message.answer("Данные профиля обновлены.\n"
                              f"User ID: {call.from_user.id}\n"
                              f"Адрес доставки: {loc_data['local_object_name']}\n"
                              f"Параметры доставки: Не указаны\n",
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [
                                      InlineKeyboardButton(
                                          text='Изменить',
                                          callback_data='change_profile'
                                      )
                                  ]
                              ]
                              ))
    await state.finish()


@dp.callback_query_handler(text='address_later', state=ProfileState.WaitAddress)
async def set_change_profile_without_address(call: CallbackQuery, state: FSMContext):
    """Обновляем данные профиля без адреса"""
    data = await state.get_data()
    local_object_id = data.get('local_object_id')
    loc_data = await db.get_local_object_data_by_id(local_object_id)
    await db.update_user_info_without_address(call.from_user.id,
                                              loc_data['local_object_metro_id'],
                                              loc_data['local_object_location_id'],
                                              local_object_id
                                              )
    await db.clear_cart(call.from_user.id)
    await db.clear_empty_orders(call.from_user.id)
    await call.message.answer("Данные профиля обновлены.\n"
                              f"User ID: {call.from_user.id}\n"
                              f"Адрес доставки: {loc_data['local_object_name']}\n"
                              f"Параметры доставки: Не указаны\n",
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [
                                      InlineKeyboardButton(
                                          text='Изменить',
                                          callback_data='change_profile'
                                      )
                                  ]
                              ]
                              ))
    await state.finish()


@dp.message_handler(state=ProfileState.WaitAddress)
async def set_change_profile(message: types.Message, state: FSMContext):
    """Обновляем данные пользователя в бд"""
    data = await state.get_data()
    local_object_id = data.get('local_object_id')
    loc_data = await db.get_local_object_data_by_id(local_object_id)
    await db.update_user_info(message.from_user.id,
                              loc_data['local_object_metro_id'],
                              loc_data['local_object_location_id'],
                              local_object_id,
                              message.text
                              )
    await db.clear_cart(message.from_user.id)
    await db.clear_empty_orders(message.from_user.id)
    await message.answer("Данные профиля обновлены.\n"
                         f"User ID: {message.from_user.id}\n"
                         f"Адрес доставки: {loc_data['local_object_name']}\n"
                         f"Параметры доставки: {message.text}\n",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [
                                 InlineKeyboardButton(
                                     text='Изменить',
                                     callback_data='change_profile'
                                 )
                             ]
                         ]
                         ))
    await state.finish()
