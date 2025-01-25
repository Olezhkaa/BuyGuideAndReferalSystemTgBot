
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram import Router
from aiogram.enums import ContentType
from aiogram.types import WebAppInfo

from db_handler.database import get_user_by_id, update_user_balance_minus
from keyboards.keyboards import out_money_get_card
from utils.payments.withdrawal import make_payout_card

router = Router()

@router.callback_query(lambda call: call.data == "out_money")
async def out_money_test(call):
    user = get_user_by_id(call.from_user.id)
    if int(user[2]) < 2500:
        await call.message.answer("❌ У вас недостаточно средств ❌\n\n"
                                  "<i>Для вывода необходимо минимум 2500 RUB</i>", reply_markup=types.ReplyKeyboardRemove())
    else:
        await call.message.answer(f"💸 <b>Вывод средств</b> 💸\n\n"
                                  f"<i>Нажмите кнопку ниже, чтобы вывести деньги на карту банка</i>",
                                  reply_markup=out_money_get_card())

# Обработка данных из WebApp
@router.message(F.content_type == ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    try:
        # Получение данных из WebApp
        data = message.web_app_data.data
        parsed_data = eval(data)  # Парсинг данных (предполагаем JSON-строку)
        payout_token = parsed_data.get("payout_token")

        user_id = message.from_user.id
        user = get_user_by_id(user_id)
        amount = user[2]

        if amount < 2500:
            await message.answer("❌ У вас недостаточно средств ❌\n\n"
                                 "<i>Для вывода необходимо минимум 2500 RUB</i>")
            return

        if payout_token:
            # Ответ пользователю с полученным токеном
            response = await make_payout_card(payout_token, amount, "Вывод средств")

            # Обрабатываем результатx
            if "error" not in response:
                await message.answer(
                    f"✅ Выплата выполнена успешно: ✅\n\n"
                    #f"ID выплаты: {response['id']}\n"
                    f"Сумма: {response['amount']['value']} {response['amount']['currency']}\n"
                    f"Статус: {response['status']}\n"
                    f"Описание: {response['description']}\n", reply_markup=types.ReplyKeyboardRemove())

                update_user_balance_minus(id_user_tg=user_id, amount_withdrawal=amount)
            else:
                await message.answer(f"Ошибка при выполнении выплаты:\n{response['error']}", reply_markup=types.ReplyKeyboardRemove())

        else:
            await message.answer("Ошибка: токен не найден в данных.", reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        await message.answer(f"Ошибка обработки данных: {str(e)}", reply_markup=types.ReplyKeyboardRemove())




#async def withdrawal_balance_callback(call, payout_token):
#     # Пример данных для теста
#     account_number = "4100116075156746"  # Тестовый кошелек
#     amount = 100.00  # Сумма выплаты
#     description = "Тестовая выплата"
#
#     # Выполняем тестовую выплату
#     response = await make_payout_yoomoney(account_number, amount, description)
#
#     # Обрабатываем результат
#     if "error" not in response:
#         await call.message.answer(
#             f"Выплата выполнена успешно:\n"
#             f"ID выплаты: {response['id']}\n"
#             f"Сумма: {response['amount']['value']} {response['amount']['currency']}\n"
#             f"Статус: {response['status']}\n"
#             f"Описание: {response['description']}\n"
#             f"Тестовый режим: {response['test']}"
#         )
#     else:
#         await call.message.answer(f"Ошибка при выполнении выплаты:\n{response['error']}")
