import logging
from gc import callbacks

from aiogram import Bot, Dispatcher, types, Router


from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

from config import DATABASE
from db_handler.database import get_user_by_id
from keyboards.keyboards import check_promo_code

route = Router()

@route.callback_query(lambda call: call.data == "by_guide")
async def purchase_guide(call):
    user_id = call.from_user.id
    guide_purchased = get_user_by_id(user_id)[5]
    #guide_purchased = False


    if guide_purchased:
        await call.message.answer("❌ Гайд уже куплен. ❌\nВведите команду: /start")
    else:
        await call.message.answer("У вас есть промокод?", reply_markup=check_promo_code())
