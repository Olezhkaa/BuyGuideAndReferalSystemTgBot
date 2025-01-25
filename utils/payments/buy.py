import logging
import sqlite3

from aiogram import types, Router, Bot, F
import json

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.types import PreCheckoutQuery, FSInputFile

from config import CURRENCY, WALLET_TOKEN_BUY, BOT_TOKEN, DATABASE, AMOUNT
from db_handler.database import get_promo_by_code
from keyboards.keyboards import payment_keyboard

router = Router()

bot = Bot(token=BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def bot_send_invoice_buy_course(chat_id, amount, promo_code):
    prices = [types.LabeledPrice(label=CURRENCY, amount=amount*100)]

    provider_data = {
        "receipt": {
            "items": [
                {
                    "description": "Курс",
                    "quantity": "1.00",
                    "amount": {
                        "value": f"{amount:.2f}",
                        "currency": CURRENCY
                    },
                    "vat_code": 1
                }
            ]
        }
    }
    provider_data = json.dumps(provider_data)

    await bot.send_invoice(
        chat_id=chat_id,
        title="Курс",
        description="Покупай курс и начинай зарабатывать деньги!",
        payload=promo_code,
        provider_token=WALLET_TOKEN_BUY,
        currency=CURRENCY,
        prices=prices,
        reply_markup=payment_keyboard(amount),
        need_phone_number = True,
        send_phone_number_to_provider = True,
        provider_data = provider_data
    )


@router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    try:
       await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)  # всегда отвечаем утвердительно
    except Exception as e:
        logging.error(f"Ошибка при обработке апдейта типа PreCheckoutQuery: {e}")

@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def handle_successful_payment(message: types.Message):
    user_id = message.from_user.id
    payment_id = message.successful_payment.provider_payment_charge_id
    amount = message.successful_payment.total_amount/100
    promo_code = message.successful_payment.invoice_payload or None

    file = FSInputFile('file/Купленный_курс.pdf', filename="Купленный гайд.pdf")
    await message.answer_document(file, protect_content=True)
    file_text = "📦 <b>Товар включает файл:</b>" if file else "📄 <b>Товар не включает файлы:</b>"
    product_text = (
        f"🎉 <b>Спасибо за покупку!</b>\n\n"
        f"🛒 <b>Информация о вашем товаре:</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🔹 <b>Название:</b> <b>Гайд</b>\n"
        f"🔹 <b>Описание:</b>\n<i>Гайд по заработку!</i>\n"
        f"🔹 <b>Цена:</b> <b>{amount}₽</b>\n"
        f"🔹 <b>Закрытое описание:</b>\n<i>Гайд был составлен Иваном</i>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"{file_text}\n\n"
        f"ℹ️ <b>Можете продолжать работать в боте.</b>"
    )

    if promo_code != 'None':
        promo = get_promo_by_code(promo_code)
        discount = promo[1]  # Скидка
        ref_by = promo[2]  # ID владельца промокода
        save_db(user_id, payment_id, amount, discount, ref_by)
    else: save_db(user_id, payment_id, amount,0, None)


    await message.answer("✅ Оплата принята!")
    await message.answer(f"{product_text}")

def save_db(user_id, payment_id, amount, discount, ref_by):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Обновление информации о покупке
    cursor.execute("UPDATE users SET course_purchased = TRUE, ref_by = ? WHERE id_user_tg = ?", (ref_by, user_id))
    cursor.execute("INSERT INTO transactions (user_id, payment_id, amount, type) VALUES (?, ?, ?, ?)",
                   (user_id, payment_id, amount, 'purchase'))

    # Начисление реферального бонуса
    if ref_by:
        referral_bonus = amount/(100 - discount) * 100 * 0.25
        cursor.execute("UPDATE users SET balance = balance + ? WHERE id_user_tg = ?", (referral_bonus, ref_by))
        cursor.execute("INSERT INTO transactions (user_id, payment_id, amount, type) VALUES (?, ?, ?, ?)",
                       (ref_by, payment_id, referral_bonus, 'referral_reward'))

    connection.commit()
    cursor.close()
    connection.commit()




