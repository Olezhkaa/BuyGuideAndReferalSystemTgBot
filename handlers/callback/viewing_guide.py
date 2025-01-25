from aiogram import Router
from aiogram.types import FSInputFile

from db_handler.database import get_user_by_id

router = Router()

@router.callback_query(lambda call: call.data == "viewing_guide")
async def viewing_guid_callback(call):
    user_id = call.from_user.id
    course_purchased = get_user_by_id(user_id)[5]

    if course_purchased:
        file = FSInputFile('file/Купленный_курс.pdf', filename="Купленный гайд.pdf")
        text = f"<b>После покупки вы всегда можете ознакомиться с купленным курсом на этой вкладке</b>"
        await call.message.answer_document(file, protect_content=True)
        await call.message.answer(text)
    else:
        await call.message.answer("❌ Курс еще не куплен. ❌\nВведите команду: /start")