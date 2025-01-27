from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from pyexpat.errors import messages

from db_handler.database import get_user_by_id
from filters.admin import check_admin
from keyboards.keyboards import main_menu_button
from db_handler import database

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    have_bought_guide = False

    if not database.user_exist(user_id):
        database.insert_user(user_id, user_full_name)
        #database.insert_promo_code(promo, 50, user_id)
    else:
        have_bought_guide = get_user_by_id(message.from_user.id)[5]

    await message.answer("Добро пожаловать! \nВыберите одну из функций:",  reply_markup=main_menu_button(have_bought_guide, check_admin(user_id)))


import string, random
def generate_promo_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))