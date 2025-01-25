from types import NoneType

from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import AMOUNT
from db_handler.database import get_promo_by_code
from utils.payments.buy import bot_send_invoice_buy_course

router = Router()

class FormByCourse(StatesGroup):
    waiting_for_promo_code = State()

@router.callback_query(lambda call: call.data == "check_promo")
async def check_promo_callback(call, state: FSMContext):
    await call.message.answer("Введите промокод:")
    await state.set_state(FormByCourse.waiting_for_promo_code)

@router.message(StateFilter(FormByCourse.waiting_for_promo_code))
async def waiting_for_promo(message: types.Message, state: FSMContext):
    promo_code = str(message.text).strip()

    promo = get_promo_by_code(promo_code)

    if not promo:
        await message.answer("❌ Неверный промокод. Попробуйте снова ❌"
                             "\nВведите команду: /start")
        await state.clear()
        return

    await state.clear()
    await bot_send_invoice_buy_course(message.from_user.id, AMOUNT/2, promo_code=promo_code)