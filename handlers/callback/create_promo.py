from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db_handler.database import get_promo_by_code, update_user_promo, insert_promo_code, get_code_by_user_id, \
    update_promo_code, get_user_by_id
from filters.admin import check_admin

router = Router()

class FormByPromo(StatesGroup):
    creating_promo = State()

@router.callback_query(lambda call: call.data == "create_promo")
async def create_promo_callback(call, state: FSMContext):
    if get_user_by_id(call.from_user.id)[5] or check_admin(call.from_user.id):
        buttons = [[types.KeyboardButton(text='❌ Отмена ❌')],]
        markup = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
        await call.message.answer("<b>Создание промокода</b>\n\n"
                                  "Введите желанный промокод:", reply_markup=markup)
        await state.set_state(FormByPromo.creating_promo)
    else:
        await call.message.answer("❌ Гайд еще не куплен. ❌\nВведите команду: /start")
        await state.clear()
        return



@router.message(StateFilter(FormByPromo.creating_promo))
async def create_promo(message: types.Message, state: FSMContext):

    if message.text == "Отмена" or message.text == "❌ Отмена ❌":
        await message.answer("<b>Отмена действия</b>\n\n"
                             "<i>Введите команду /start</i>", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return

    promo_code = str(message.text).strip()

    promo = get_promo_by_code(promo_code)

    user_id = message.from_user.id

    if not promo:
        update_user_promo(user_id, promo_code)
        row_promo_code = get_code_by_user_id(user_id)
        if row_promo_code is None:
            insert_promo_code(promo_code, 50, user_id)
        else: update_promo_code(user_id, promo_code)

        await message.answer("✅ Промокод успешно создан! ✅", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("❌ Данный промокод уже существует. Попробуйте снова ❌"
                             "\nВведите команду: /start", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return

    await state.clear()