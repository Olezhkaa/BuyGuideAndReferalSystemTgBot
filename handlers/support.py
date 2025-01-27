from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command('support'))
async def help_command(message: types.Message):
    text = (f'<b>🛠️ Техническая поддержка 🛠️</b>\n\n'
            f'❗ Если у вас возникли трудности с пользованием телеграмм бота\n'
            f'❗ Проблемы с оплатой или выплатой\n'
            f'❗ Обратитесь в службу технической поддержки, используя контакты ниже!\n\n'
            f'<b>📱 Контакты для связи:</b>\n'
            f'<b>Электронная почта:</b> ...\n')

    await message.answer(text=text)