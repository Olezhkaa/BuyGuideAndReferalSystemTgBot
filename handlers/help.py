from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command('help'))
async def help_command(message: types.Message):
    text = (f'<b>📑 Помощь 📑</b>\n\n'
            f'<b>🔻 Команды:</b>\n'
            f'🧷 /start - Начало работы\n'
            f'🧷 /support - Техническая поддержка\n'
            f'🧷 /help - Помощь\n\n'
            f'<b>©️ Разработчик:</b> <i>Фадеев Олег Григорьевич</i>\n'
            f'<b>📌 Телеграмм:</b> <i>@Oleg_Fadeev_Dev</i>\n'
            f'<b>📌 Вконтакте:</b> <i>@Oleg_Fadeev</i>')

    await message.answer(text=text)