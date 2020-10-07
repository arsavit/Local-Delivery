import logging

from keyboards.default.menu import menu_keyboard
from loader import db
from states.admin_state import AddAdmin
from states.bonus_state import Bonus
from states.menu_states import Menu, SignUpUser
from states.profile_states import ProfileState
from states.seller_admin_states import SellerAdmin
from states.sellers_states import SelectCourier

states_for_menu = [ProfileState.WaitAddress,
                   Menu.WaitAddress,
                   Menu.WaitTime,
                   Menu.WaitCategory,
                   Menu.WaitProduct,
                   Menu.WaitProductSize,
                   Menu.WaitProductSizeBack,
                   Menu.OneMoreOrNext,
                   Menu.WaitUserConfirmationDelivery,
                   Menu.WaitUserConfirmationPickup,
                   Menu.WaitPass,
                   Menu.WaitQuantity,
                   Menu.WaitQuantity6,
                   Menu.WaitQuantityFromSize,
                   Menu.WaitQuantityBack,
                   Menu.WaitQuantity6Back,
                   Menu.WaitQuantityBackWithSizeId,
                   Menu.WaitQuantity6BackWithSize,
                   Menu.WaitQuantity6BackWithSizeId,
                   Menu.WaitQuantityBackWithSize,
                   SignUpUser.Metro,
                   ProfileState.WaitMetro,
                   ProfileState.WaitLocation,
                   SellerAdmin.RemoveItemFromStockCategory,
                   SellerAdmin.ReturnItemToStockCategory,
                   AddAdmin.WaitDeleteAdmins,
                   AddAdmin.WaitDeleteMetro,
                   AddAdmin.NewLocationMetro,
                   AddAdmin.SaveNewLocation,
                   AddAdmin.LocalObjectMetro,
                   AddAdmin.LocalObjectLocation,
                   AddAdmin.LocalObjectNameMore,
                   AddAdmin.OneMoreNewCategory,
                   AddAdmin.ItemCategory,
                   AddAdmin.ItemSize,
                   AddAdmin.ItemSizeConfirmFirst,
                   AddAdmin.ItemSizeConfirm,
                   AddAdmin.OneMoreProductSize,
                   AddAdmin.ItemConfirm,
                   AddAdmin.RemoveItemCategory,
                   AddAdmin.AdminSellerMetro,
                   AddAdmin.AdminSellerLocation,
                   AddAdmin.SellerMetro,
                   AddAdmin.SellerLocation,
                   AddAdmin.CourierMetro,
                   AddAdmin.CourierLocation,
                   AddAdmin.RemoveItemFromStockCategory,
                   AddAdmin.ReturnItemToStockCategory,
                   AddAdmin.ChangeSellerAdminMetro,
                   AddAdmin.ChangeSellerAdminLocation,
                   AddAdmin.ChangeSellerMetro,
                   AddAdmin.ChangeSellerLocation,
                   AddAdmin.ChangeCourierMetro,
                   AddAdmin.ChangeCourierLocation,
                   AddAdmin.EditMetro,
                   AddAdmin.EditItem,
                   AddAdmin.EditItemByWaitSubject,
                   AddAdmin.EditItemByAvailability,
                   AddAdmin.EditItemBySizes,
                   AddAdmin.EditItemEditSizeById,
                   Bonus.Count,
                   AddAdmin.EditDeliveryItem,
                   AddAdmin.EditDeliveryItemID,
                   AddAdmin.EditDeliveryItemPrice,
                   AddAdmin.ReturnDeliveryItemToStockCategory,
                   AddAdmin.ReturnDeliveryItemToStockProduct,
                   AddAdmin.RemoveDeliveryItemFromStockCategory,
                   AddAdmin.RemoveDeliveryItemFromStockProduct,
                   AddAdmin.RemoveDeliveryItemCat,
                   AddAdmin.RemoveDeliveryItem,
                   AddAdmin.RemoveDeliveryCategory,
                   AddAdmin.TakeOrders,
                   AddAdmin.TakeOrdersWait,
                   AddAdmin.DeliveryCategoryName,
                   AddAdmin.DeliveryItemCategory,
                   AddAdmin.DeliveryItemName,
                   AddAdmin.DeliveryItemPrice,
                   SellerAdmin.ChangeOrder,
                   SellerAdmin.DeliveryCategory,
                   SellerAdmin.ChangeDeliveryDate,
                   SellerAdmin.WaitCancelConfirm,
                   SellerAdmin.ChangeDeliveryTime,
                   SellerAdmin.ChangeDeliveryConfirm,
                   SellerAdmin.ChangeDeliveryWaitConfirm,
                   SellerAdmin.DeliveryProduct,
                   SellerAdmin.DeliveryQuantity,
                   SellerAdmin.DeliveryQuantity6,
                   SellerAdmin.ConfirmTempOrder,
                   SellerAdmin.ConfirmTempOrderRemoved,
                   SellerAdmin.DeliveryDate,
                   SellerAdmin.DeliveryTime,
                   SellerAdmin.ConfirmOrder,
                   Menu.OrderStatus,
                   Menu.WaitReasonUser,
                   SelectCourier.WaitReasonCourier,
                   Menu.WaitReview,
                   SelectCourier.WaitReasonActive,
                   SelectCourier.WaitReason]


async def reset_state(state, message):
    """обрабатываем выход из меню"""
    if await state.get_state() in ['ProfileState:WaitAddress', 'Menu:WaitCategory',
                                   'Menu:WaitProduct', 'Menu:WaitProductSize', 'Menu:WaitProductSizeBack',
                                   'Menu:OneMoreOrNext', 'Menu:WaitQuantity', 'Menu:WaitQuantity6',
                                   'Menu:WaitQuantityFromSize', 'Menu:WaitQuantityBack', 'Menu:WaitQuantity6Back',
                                   'Menu:WaitQuantityBackWithSizeId', 'Menu:WaitQuantity6BackWithSize',
                                   'Menu.WaitQuantity6BackWithSizeId', 'Menu:WaitQuantityBackWithSize',
                                   'SignUpUser:Metro', 'ProfileState:WaitMetro', 'ProfileState:WaitLocation',
                                   'ProfileState:WaitAddress', 'SellerAdmin:RemoveItemFromStockCategory',
                                   'SellerAdmin:ReturnItemToStockCategory', 'AddAdmin:WaitDeleteAdmins',
                                   'AddAdmin:WaitDeleteMetro', 'AddAdmin:NewLocationMetro',
                                   'AddAdmin:SaveNewLocation', 'AddAdmin:LocalObjectMetro',
                                   'AddAdmin:LocalObjectLocation', 'AddAdmin:LocalObjectNameMore',
                                   'AddAdmin:OneMoreNewCategory', 'AddAdmin:ItemCategory',
                                   'AddAdmin:ItemSize', 'AddAdmin:ItemSizeConfirmFirst',
                                   'AddAdmin:ItemSizeConfirm', 'AddAdmin:OneMoreProductSize',
                                   'AddAdmin:ItemConfirm', 'AddAdmin:RemoveItemCategory',
                                   'AddAdmin:AdminSellerMetro', 'AddAdmin:AdminSellerLocation',
                                   'AddAdmin:SellerMetro', 'AddAdmin:SellerLocation',
                                   'AddAdmin:CourierMetro', 'AddAdmin:CourierLocation',
                                   'AddAdmin:RemoveItemFromStockCategory', 'AddAdmin:ReturnItemToStockCategory',
                                   'AddAdmin:ChangeSellerAdminMetro', 'AddAdmin:ChangeSellerAdminLocation',
                                   'AddAdmin:ChangeSellerMetro', 'AddAdmin:ChangeSellerLocation',
                                   'AddAdmin:ChangeCourierMetro', 'AddAdmin:ChangeCourierLocation',
                                   'AddAdmin:EditMetro', 'AddAdmin:EditItem',
                                   'AddAdmin:EditItemByWaitSubject', 'AddAdmin:EditItemByAvailability',
                                   'AddAdmin:EditItemBySizes', 'AddAdmin:EditItemEditSizeById',
                                   'Bonus:Count', 'AddAdmin:EditDeliveryItem', 'AddAdmin:EditDeliveryItemID',
                                   'AddAdmin:EditDeliveryItemPrice', 'AddAdmin:ReturnDeliveryItemToStockCategory',
                                   'AddAdmin:ReturnDeliveryItemToStockProduct',
                                   'AddAdmin:RemoveDeliveryItemFromStockCategory',
                                   'AddAdmin:RemoveDeliveryItemFromStockProduct', 'AddAdmin:RemoveDeliveryItemCat',
                                   'AddAdmin:RemoveDeliveryItem', 'AddAdmin.RemoveDeliveryCategory',
                                   'AddAdmin:TakeOrders', 'AddAdmin:TakeOrdersWait', 'AddAdmin:DeliveryCategoryName',
                                   'AddAdmin:DeliveryItemCategory', 'AddAdmin:DeliveryItemName',
                                   'AddAdmin:DeliveryItemPrice', 'SellerAdmin:ChangeOrder',
                                   'SellerAdmin:ChangeDeliveryDate',
                                   'SellerAdmin:WaitCancelConfirm', 'SellerAdmin:ChangeDeliveryTime',
                                   'SellerAdmin:ChangeDeliveryConfirm', 'SellerAdmin:ChangeDeliveryWaitConfirm']:
        await state.finish()
    elif await state.get_state() in ['Menu:OrderStatus', 'Menu:WaitReasonUser', 'SelectCourier:WaitReasonCourier',
                                     'SelectCourier:WaitReason', 'SelectCourier:WaitReasonActive']:
        await state.finish()
        await message.answer('Заказ не отменен',
                             reply_markup=menu_keyboard)
    elif await state.get_state() in ['Menu:WaitReview']:
        await state.finish()
        await message.answer('Отзыв не сохранен',
                             reply_markup=menu_keyboard)
    elif await state.get_state() in ['SellerAdmin:DeliveryCategory', 'SellerAdmin:DeliveryProduct',
                                     'SellerAdmin:DeliveryQuantity', 'SellerAdmin:DeliveryQuantity6',
                                     'SellerAdmin:ConfirmTempOrder', 'SellerAdmin:ConfirmTempOrderRemoved',
                                     'SellerAdmin:DeliveryDate', 'SellerAdmin:DeliveryTime',
                                     'SellerAdmin:ConfirmOrder']:
        await state.finish()
        await db.delete_temp_delivery_order_by_user_id(message.from_user.id)
    elif await state.get_state() in ['Menu:WaitTime', 'Menu:WaitUserConfirmationDelivery',
                                     'Menu:WaitUserConfirmationPickup', 'Menu:WaitPass',
                                     'Menu:WaitAddress']:
        await state.finish()
        order_id = await db.get_last_order_id(message.from_user.id)
        await db.delete_order_by_id(order_id)
