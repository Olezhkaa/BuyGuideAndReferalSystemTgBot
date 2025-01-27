from aiogram import types, Router

from config import AMOUNT
from utils.payments.buy import bot_send_invoice_buy_guide

router = Router()

@router.callback_query(lambda call: call.data == "no_promo")
async def no_guide_callback(call):
    await bot_send_invoice_buy_guide(call.from_user.id, AMOUNT, "None")