from aiogram import Bot, Dispatcher, types, Router
import sqlite3

from config import DATABASE
from db_handler.database import get_user_by_id
from keyboards.keyboards import balance_out_money

router = Router()

@router.callback_query(lambda call: call.data == "balance")
async def check_balance(call):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    user_id = call.from_user.id
    cursor.execute("SELECT balance FROM users WHERE id_user_tg = (?)", (user_id,))
    balance = cursor.fetchone()

    text = (f"<b>Баланс</b>\n\n"
            f"Ваш текущий баланс: {balance[0]} RUB")


    await call.message.answer(text=text, reply_markup=balance_out_money())