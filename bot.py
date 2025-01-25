import logging
import sys
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import handlers.handlers
from config import BOT_TOKEN

import db_handler.database

#from utils.payments.buy import create_payment_link
#from aiogram.filters import Command

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()



async def main() -> None:
    logging.info("Бот активирован")
    db_handler.database.init_db()
    await handlers.handlers.include_routers_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())