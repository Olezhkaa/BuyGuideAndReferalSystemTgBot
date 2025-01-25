from aiogram import types, Router

from config import AMOUNT
from utils.payments.buy import bot_send_invoice_buy_course

router = Router()

@router.callback_query(lambda call: call.data == "no_promo")
async def no_course_callback(call):
    await bot_send_invoice_buy_course(call.from_user.id, AMOUNT, "None")