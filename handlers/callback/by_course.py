import logging
from gc import callbacks

from aiogram import Bot, Dispatcher, types, Router
import sqlite3

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

from config import DATABASE
from db_handler.database import get_user_by_id
from keyboards.keyboards import check_promo_code

route = Router()

@route.callback_query(lambda call: call.data == "by_course")
async def purchase_course(call, state: FSMContext):
    user_id = call.from_user.id
    course_purchased = get_user_by_id(user_id)[5]
    #course_purchased = False


    if course_purchased:
        await call.message.answer("❌ Курс уже куплен. ❌\nВведите команду: /start")
    else:
        await call.message.answer("У вас есть промокод?", reply_markup=check_promo_code())
