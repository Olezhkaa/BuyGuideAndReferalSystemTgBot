from types import NoneType

from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import AMOUNT
from db_handler.database import get_promo_by_code
from utils.payments.buy import bot_send_invoice_buy_guide

router = Router()

class FormByGuide(StatesGroup):
    waiting_for_promo_code = State()

@router.callback_query(lambda call: call.data == "check_promo")
async def check_promo_callback(call, state: FSMContext):
    buttons = [[types.KeyboardButton(text='❌ Отмена ❌')], ]
    markup = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)

    await call.message.answer("Введите промокод:", reply_markup=markup)
    await state.set_state(FormByGuide.waiting_for_promo_code)

@router.message(StateFilter(FormByGuide.waiting_for_promo_code))
async def waiting_for_promo(message: types.Message, state: FSMContext):

    if message.text == "Отмена" or message.text == "❌ Отмена ❌":
        await message.answer("<b>Отмена действия</b>\n\n"
                             "<i>Введите команду /start</i>", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return

    promo_code = str(message.text).strip()

    promo = get_promo_by_code(promo_code)

    if not promo:
        await message.answer("❌ Неверный промокод. Попробуйте снова ❌"
                             "\nВведите команду: /start")
        await state.clear()
        return

    await state.clear()
    await bot_send_invoice_buy_guide(message.from_user.id, AMOUNT/2, promo_code=promo_code)