import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import page_call_data, metro_del_data
from keyboards.inline.inline_keyboards import generate_key_board_with_admins, generate_key_board_with_metro, \
    generate_key_board_with_locations, generate_keyboard_with_categories_for_add_item, get_available_local_objects, \
    generate_keyboard_with_categories, generate_keyboard_with_products, get_available_local_objects_profile, \
    generate_keyboard_with_metro_for_seller_admin, generate_keyboard_with_metro, generate_keyboard_with_metro_profile, \
    generate_keyboard_with_delivery_categories_for_add_item
from keyboards.inline.statistics_keyboards import gen_years_keyboard
from loader import dp, db
from states.admin_state import AddAdmin
from states.menu_states import SignUpUser, Menu
from states.profile_states import ProfileState
from states.seller_admin_states import SellerAdmin


@dp.callback_query_handler(page_call_data.filter(), state=[SellerAdmin.Year,
                                                           SellerAdmin.Month])
async def get_admin_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка админов"""
    page = int(callback_data.get('page'))
    years = await db.get_orders_years()
    await call.message.edit_reply_markup(await gen_years_keyboard(years, page))


@dp.callback_query_handler(page_call_data.filter(), state=AddAdmin.WaitDeleteAdmins)
async def get_admin_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка админов"""
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_key_board_with_admins(page))


@dp.callback_query_handler(page_call_data.filter(), state=[AddAdmin.WaitDeleteMetro,
                                                           AddAdmin.NewLocationMetro,
                                                           AddAdmin.LocalObjectMetro,
                                                           AddAdmin.EditMetro,
                                                           AddAdmin.ChangeSellerAdminMetro,
                                                           AddAdmin.ChangeSellerMetro,
                                                           AddAdmin.ChangeCourierMetro])
async def get_metro_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка метро"""
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_key_board_with_metro(page))


@dp.callback_query_handler(page_call_data.filter(), state=[AddAdmin.AdminSellerMetro,
                                                           AddAdmin.SellerMetro,
                                                           AddAdmin.CourierMetro])
async def get_metro_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка метро"""
    page = int(callback_data.get('page'))
    logging.info(page)
    await call.message.edit_reply_markup(await generate_keyboard_with_metro_for_seller_admin(page))


@dp.callback_query_handler(page_call_data.filter(), state=[SignUpUser.Metro,])
async def get_metro_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка метро"""
    page = int(callback_data.get('page'))
    logging.info(page)
    await call.message.edit_reply_markup(await generate_keyboard_with_metro(page))


@dp.callback_query_handler(page_call_data.filter(), state=[ProfileState.WaitMetro])
async def get_metro_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка метро"""
    page = int(callback_data.get('page'))
    logging.info(page)
    await call.message.edit_reply_markup(await generate_keyboard_with_metro_profile(page))


@dp.callback_query_handler(page_call_data.filter(), state=[AddAdmin.AdminSellerLocation,
                                                           AddAdmin.SellerLocation,
                                                           AddAdmin.CourierLocation,
                                                           AddAdmin.ChangeSellerAdminLocation,
                                                           AddAdmin.ChangeSellerLocation,
                                                           AddAdmin.ChangeCourierLocation])
async def get_location_pagination_list(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Пагинация списка локаций"""
    data = await state.get_data()
    metro_id = data.get('metro_id')
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_key_board_with_locations(metro_id, page))


@dp.callback_query_handler(page_call_data.filter(), state=AddAdmin.LocalObjectLocation)
async def get_location_pagination_list(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Пагинация списка локаций"""
    data = await state.get_data()
    metro_id = data.get('new_local_object')['metro_id']
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_key_board_with_locations(metro_id, page))


@dp.callback_query_handler(page_call_data.filter(), state=[SignUpUser.Location])
async def get_metro_pagination_list(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Пагинация списка локальных объектов"""
    data = await state.get_data()
    metro_id = data.get('metro_id')
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await get_available_local_objects(metro_id, page))


@dp.callback_query_handler(page_call_data.filter(), state=[ProfileState.WaitLocation])
async def get_metro_pagination_list(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Пагинация списка локальных объектов"""
    data = await state.get_data()
    metro_id = data.get('metro_id')
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await get_available_local_objects_profile(metro_id, page))


@dp.callback_query_handler(page_call_data.filter(), state=[AddAdmin.ItemCategory,
                                                           AddAdmin.RemoveItemCategory])
async def get_category_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка категорий"""
    categories = await db.get_list_of_categories()
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_keyboard_with_categories_for_add_item(categories, page))


@dp.callback_query_handler(page_call_data.filter(), state=Menu.WaitCategory)
async def get_category_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка категорий"""
    category_list = await db.get_categories_for_user_location_id(call.from_user.id)
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_keyboard_with_categories(category_list, page))


@dp.callback_query_handler(page_call_data.filter(), state=SellerAdmin.EditItemPriceCommand)
async def get_category_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка категорий"""
    category_list = await db.get_list_of_categories_with_items()
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_keyboard_with_categories(category_list, page))


@dp.callback_query_handler(page_call_data.filter(), state=AddAdmin.RemoveItemFromStockCategory)
async def get_category_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка категорий"""
    category_list = await db.get_category_for_remove_item_from_stock()
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_keyboard_with_categories_for_add_item(category_list, page))


@dp.callback_query_handler(page_call_data.filter(), state=[SellerAdmin.RemoveItemFromStockCategory,])
async def get_category_pagination_list(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Пагинация списка категорий"""
    data = await state.get_data()
    location_id = data.get('location_id')
    category_list = await db.get_category_for_stock_item_in_location(location_id, 'true')
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_keyboard_with_categories_for_add_item(category_list, page))


@dp.callback_query_handler(page_call_data.filter(), state=[SellerAdmin.ReturnItemToStockCategory,])
async def get_category_pagination_list(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Пагинация списка категорий"""
    data = await state.get_data()
    location_id = data.get('location_id')
    category_list = await db.get_category_for_stock_item_in_location(location_id, 'false')
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_keyboard_with_categories_for_add_item(category_list, page))


@dp.callback_query_handler(page_call_data.filter(), state=AddAdmin.ReturnItemToStockCategory)
async def get_category_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка категорий"""
    category_list = await db.get_category_for_admin()
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_keyboard_with_categories_for_add_item(category_list, page))


@dp.callback_query_handler(page_call_data.filter(), state=[AddAdmin.DeliveryItemCategory,
                                                           AddAdmin.RemoveDeliveryItemCat,
                                                           AddAdmin.RemoveDeliveryItemFromStockCategory])
async def get_category_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка категорий"""
    category_list = await db.get_list_of_delivery_categories()
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_keyboard_with_delivery_categories_for_add_item(category_list, page))


@dp.callback_query_handler(page_call_data.filter(), state=AddAdmin.EditItem)
async def get_category_pagination_list(call: CallbackQuery, callback_data: dict):
    """Пагинация списка категорий"""
    categories = await db.get_categories_with_products()
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_keyboard_with_categories_for_add_item(categories, page))


@dp.callback_query_handler(page_call_data.filter(), state=Menu.WaitProduct)
async def get_product_pagination_list(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Пагинация списка товаров"""
    data = await state.get_data()
    category_id = data.get('category_id')
    products = await db.get_product_for_user_location_id(call.from_user.id, category_id)
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_keyboard_with_products(products, page))


@dp.callback_query_handler(page_call_data.filter(), state=SellerAdmin.EditItemPriceCategory)
async def get_product_pagination_list(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Пагинация списка товаров в категории при изменения цены товара в локации"""
    data = await state.get_data()
    category_id = data.get('category_id')
    products = await db.get_products_list(category_id)
    page = int(callback_data.get('page'))
    await call.message.edit_reply_markup(await generate_keyboard_with_products(products, page))












