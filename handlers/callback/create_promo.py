from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db_handler.database import get_promo_by_code, update_user_promo, insert_promo_code, get_code_by_user_id, \
    update_promo_code

router = Router()

class FormByPromo(StatesGroup):
    creating_promo = State()

@router.callback_query(lambda call: call.data == "create_promo")
async def create_promo_callback(call, state: FSMContext):
    await call.message.answer("<b>Создание промокода</b>\n\n"
                              "Введите желанный промокод:")
    await state.set_state(FormByPromo.creating_promo)

@router.message(StateFilter(FormByPromo.creating_promo))
async def create_promo(message: types.Message, state: FSMContext):
    promo_code = str(message.text).strip()

    promo = get_promo_by_code(promo_code)

    user_id = message.from_user.id

    if not promo:
        update_user_promo(user_id, promo_code)
        row_promo_code = get_code_by_user_id(user_id)
        if row_promo_code is None:
            insert_promo_code(promo_code, 50, user_id)
        else: update_promo_code(user_id, promo_code)

        await message.answer("✅ Промокод успешно создан! ✅")
    else:
        await message.answer("❌ Данный промокод уже существует. Попробуйте снова ❌"
                             "\nВведите команду: /start")
        await state.clear()
        return

    await state.clear()