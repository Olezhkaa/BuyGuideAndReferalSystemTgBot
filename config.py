import json
import os

from dotenv import dotenv_values

config = dotenv_values('.env')

BOT_TOKEN = config['bot_token']

WALLET_TOKEN_BUY = config['wallet_token_buy']

YOO_KASSA_AGENT_ID_WITHDRAWAL = config['yoo_kassa_agent_id_withdrawal']
YOO_KASSA_SECRET_KEY_WITHDRAWAL = config['yoo_kassa_secret_key_withdrawal']

ADMINS = json.loads(os.environ['admins'])


AMOUNT = 840
CURRENCY = "RUB"

HOST = config['host']
USER = config['user']
PASSWORD = config['password']
DATABASE = config['database']