from aiogram import types, Router

from db_handler.database import get_user_by_id, top_promo, get_all_by_guide
from filters.admin import check_admin
from keyboards.keyboards import admin_panel_main, balance_out_money, balance_out_money_admin, out_money_get_card

router = Router()

@router.callback_query(lambda call: call.data == "admin_panel")
async def admin_panel_callback(call):

    if not check_admin(call.from_user.id):
        await call.message.answer("❌ Вы не являетесь администратором, данный функционал не доступен! ❌\n"
                                  "Введите /start и обратитесь в службу технической поддержки: OlegFadeev2000@gmail.com")
        return

    text = (f"<b>⚙️ Админ панель ⚙️</b>\n\n"
            f"<i>Это панель администрации, выберите одну из функций:</i>")

    await call.message.answer(text=text, reply_markup=admin_panel_main())

@router.callback_query(lambda call: call.data == "statistic_admin")
async def statistic_admin_callback(call):

    get_quantities_by_guide = get_all_by_guide().__len__()

    text = (f"<b>📋 Статистика 📋</b>\n\n"
            f"💸 Количество купленных гайдов: <i>{get_quantities_by_guide}</i>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📈 {check_top_promo()}")

    await call.message.answer(text=text)

    #await call.message.answer("В разработке...")

def check_top_promo():
    try:
        top_promo_codes = top_promo(5)

        if not top_promo_codes:
            return "❌ Промокоды пока не использовались! ❌"
        response = "<b>Топ 5 использованных промокодов:</b>\n\n"
        for idx, (promo_code, users_count) in enumerate(top_promo_codes, start=1):
            response += f"{idx}. Промокод: <code>{promo_code}</code> — {users_count} пользователей\n"

        return response
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

