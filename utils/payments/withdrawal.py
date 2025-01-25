import logging
import uuid
from aiogram import Bot, Dispatcher, types
import requests
import aiohttp

from config import YOO_KASSA_AGENT_ID_WITHDRAWAL, YOO_KASSA_SECRET_KEY_WITHDRAWAL

YO_KASSA_AGENT_ID = YOO_KASSA_AGENT_ID_WITHDRAWAL  # Замените на ваш agentId
YO_KASSA_SECRET_KEY = YOO_KASSA_SECRET_KEY_WITHDRAWAL  # Замените на секретный ключ

# URL для API ЮKassa
YO_KASSA_API_URL = "https://api.yookassa.ru/v3/payouts"

# Функция для выполнения выплаты через Юкасса
async def make_payout_card(payout_token, amount, description):
    """
    Выполняет выплату через API ЮKassa по payout_token.
    """
    # Формирование данных для запроса
    payout_data = {
        "payout_token": payout_token,  # Передаем токен, полученный через виджет
        "amount": {  # Параметр для суммы выплаты
            "value": f"{amount:.2f}",  # Значение суммы (строка с двумя знаками после точки)
            "currency": "RUB"  # Валюта выплаты (RUB — российский рубль)
        },
        "description": description,
    }

    # Генерация уникального Idempotence-Key
    idempotence_key = str(uuid.uuid4())  # Уникальный ключ для каждого запроса

    # Аутентификация через Basic Auth (agentId:secret_key)
    auth = aiohttp.BasicAuth(YO_KASSA_AGENT_ID, YO_KASSA_SECRET_KEY)

    async with aiohttp.ClientSession(auth=auth) as session:
        headers = {"Idempotence-Key": idempotence_key}  # Добавляем заголовок Idempotence-Key
        async with session.post(YO_KASSA_API_URL, json=payout_data, headers=headers) as response:
            if response.status == 200:
                return await response.json()  # Успешный ответ
            else:
                return {"error": await response.text()}  # Ошибка




# Функция для выполнения выплаты через Юкасса
# async def make_payout_yoomoney(account_number: str, amount: float, description: str):
#     """
#     Выполняет тестовую выплату через API ЮKassa.
#     """
#     # Формирование данных для запроса
#     payout_data = {
#         "amount": {
#             "value": f"{amount:.2f}",
#             "currency": "RUB"
#         },
#         "payout_destination_data": {
#             "type": "yoo_money",
#             f"account_number": f"{account_number}"
#         },
#         f"description": f"{description}",
#         "metadata": {
#             "order_id": "37"
#         }
#     }
#
#     # Генерация уникального Idempotence-Key
#     idempotence_key = str(uuid.uuid4())  # Уникальный ключ для каждого запроса
#
#     # Аутентификация через Basic Auth (agentId:secret_key)
#     auth = aiohttp.BasicAuth(YO_KASSA_AGENT_ID, YO_KASSA_SECRET_KEY)
#
#     async with aiohttp.ClientSession(auth=auth) as session:
#         headers = {"Idempotence-Key": idempotence_key}  # Добавляем заголовок Idempotence-Key
#         async with session.post(YO_KASSA_API_URL, json=payout_data, headers=headers) as response:
#             if response.status == 200:
#                 return await response.json()
#             else:
#                 return {"error": await response.text()}