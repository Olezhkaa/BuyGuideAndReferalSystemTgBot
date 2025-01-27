from aiogram import Router
from aiogram.types import FSInputFile

from db_handler.database import get_user_by_id
from filters.admin import check_admin

router = Router()

@router.callback_query(lambda call: call.data == "viewing_guide")
async def viewing_guid_callback(call):
    user_id = call.from_user.id
    guide_purchased = get_user_by_id(user_id)[5]

    if guide_purchased or check_admin(user_id):
        file = FSInputFile('file/Купленный_курс.pdf', filename="Купленный гайд.pdf")
        text = f"<b>После покупки вы всегда можете ознакомиться с купленным гайдом на этой вкладке</b>"
        await call.message.answer_document(file, protect_content=True)
        await call.message.answer(text)
    else:
        await call.message.answer("❌ Гайд еще не куплен. ❌\nВведите команду: /start")