
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram import Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import WebAppInfo

from db_handler.database import get_user_by_id, update_user_balance_minus
from filters.admin import check_admin
from keyboards.keyboards import out_money_get_card
from utils.payments.withdrawal import make_payout_card

router = Router()

class WithdrawalState(StatesGroup):
    payout_token = State()

@router.callback_query(lambda call: call.data == "out_money")
async def out_money_test(call):
    user = get_user_by_id(call.from_user.id)
    if user[5] or check_admin(call.from_user.id):
        if int(user[2]) < 2500 and not check_admin(call.from_user.id):
            await call.message.answer("❌ У вас недостаточно средств ❌\n\n"
                                      "<i>Для вывода необходимо минимум 2500 RUB</i>",
                                      reply_markup=types.ReplyKeyboardRemove())
        else:
            await call.message.answer(f"💸 <b>Вывод средств</b> 💸\n\n"
                                      f"<i>Нажмите кнопку ниже, чтобы вывести деньги на карту банка</i>",
                                      reply_markup=out_money_get_card())
    else:
        await call.message.answer("❌ Гайд еще не куплен. ❌\nВведите команду: /start")
        return


# Обработка данных из WebApp
@router.message(F.content_type == ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message, state: FSMContext):
    try:
        # Получение данных из WebApp
        data = message.web_app_data.data
        parsed_data = eval(data)  # Парсинг данных (предполагаем JSON-строку)
        payout_token = parsed_data.get("payout_token")

        user_id = message.from_user.id
        user = get_user_by_id(user_id)
        amount = user[2]

        if check_admin(user_id):
            buttons = [[types.InlineKeyboardButton(text="Личный баланс", callback_data="admin_balance_1")],
                       [types.InlineKeyboardButton(text="Админ баланс", callback_data="admin_balance_2")]
                       ]
            markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

            await message.answer("Выберите источник баланса для вывода:", reply_markup=markup)
            await state.update_data(payout_token=payout_token)
            return

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


@router.callback_query(F.data.in_({"admin_balance_1", "admin_balance_2"}))
async def admin_balance_choice_handler(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        balance_choice = callback_query.data

        # Получаем сохраненный payout_token из FSM
        data = await state.get_data()
        payout_token = data.get("payout_token")

        if balance_choice == "admin_balance_1":
            user_id = callback_query.from_user.id
        else:
            user_id = '0001'

        admin_amount = get_user_by_id(user_id)[2]

        if admin_amount < 100:
            await callback_query.message.answer(
                f"❌ Недостаточно средств на выбранном балансе ({balance_choice}) ❌\n"
                f"<i>Для вывода необходимо минимум 100 RUB</i>"
            )
            # Сбрасываем состояние
            await state.clear()
            return

        # Выполнение выплаты с выбранного баланса
        response = await make_payout_card(payout_token, admin_amount, f"Вывод средств с {balance_choice}")

        if "error" not in response:
            await callback_query.message.answer(
                f"✅ Выплата выполнена успешно с {balance_choice}: ✅\n\n"
                f"Сумма: {response['amount']['value']} {response['amount']['currency']}\n"
                f"Статус: {response['status']}\n"
                f"Описание: {response['description']}\n", reply_markup=types.ReplyKeyboardRemove()
            )

            # Обновляем баланс в зависимости от выбранного источника
            update_user_balance_minus(id_user_tg=user_id, amount_withdrawal=admin_amount)
        else:
            await callback_query.message.answer(
                f"Ошибка при выполнении выплаты с {balance_choice}:\n{response['error']}",
                reply_markup=types.ReplyKeyboardRemove()
            )

        # Завершаем FSM
        await state.clear()

    except Exception as e:
        await callback_query.message.answer(f"Ошибка обработки данных: {str(e)}",
                                            reply_markup=types.ReplyKeyboardRemove())
        # Завершаем FSM в случае ошибки
        await state.clear()


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
