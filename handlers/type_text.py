from aiogram import types, Router, F

from db_handler.database import update_user_balance_plus

router = Router()

@router.message(F.text == '+2500 RUB')
async def admin_money(message: types.Message):
    update_user_balance_plus(message.from_user.id, '2500')
    await message.answer("На ваш счет начислено 2500 RUB")