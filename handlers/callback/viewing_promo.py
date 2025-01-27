from aiogram import Router

from db_handler.database import get_code_by_user_id, get_user_by_id, get_users_ref_by
from keyboards.keyboards import create_promo

router = Router()

@router.callback_query(lambda call: call.data == "viewing_promo")
async def viewing_promo_callback(call):
    user_id = call.from_user.id
    user = get_user_by_id(user_id)
    promo = user[3]

    if promo is None:
        await call.message.answer("У вас еще нет промокода, нажмите кнопку ниже, чтобы создать его", reply_markup=create_promo())
    else:
        promo_c = get_code_by_user_id(user_id)
        promo_code = promo_c[0]
        discount = promo_c[1]
        quantity_users = get_users_ref_by(promo_code).__len__()
        text = ("<b>Промокод</b>\n\n"
                f"Ваш персональный промокод: <i>{promo_code}</i>\n"
                f"Предоставляемая скидка: <i>{int(discount)}%</i>\n"
                f"Количество использований: <i>{quantity_users}</i>")
        await call.message.answer(text=text, reply_markup=create_promo())