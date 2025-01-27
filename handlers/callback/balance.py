from aiogram import Bot, Dispatcher, types, Router

from db_handler.database import get_user_by_id
from filters.admin import check_admin
from keyboards.keyboards import balance_out_money

router = Router()

@router.callback_query(lambda call: call.data == "balance")
async def check_balance(call):
    user_id = call.from_user.id
    balance = get_user_by_id(user_id)[2]

    if check_admin(user_id):
        balance_admin = get_user_by_id('0001')[2]
        text = (f"<b>Баланс</b>\n\n"
                f"Ваш личный баланс: {balance} RUB\n"
                f"Админ баланс: {balance_admin} RUB")
    else:
        text = (f"<b>Баланс</b>\n\n"
                f"Ваш текущий баланс: {balance} RUB")

    await call.message.answer(text=text, reply_markup=balance_out_money())