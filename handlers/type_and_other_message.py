from aiogram import types, Router, F
from aiogram.enums import ContentType

router = Router()

@router.message(F.content_type == ContentType.TEXT)
async def message_text(message):
    await message.answer("Извините, но я вас не понимаю. Введите /help, чтобы ознакомиться с моими возможностями")

@router.message(F.content_type == ContentType.PHOTO)
async def message_phot(message):
    await message.answer("Красивая картинка, но извините, я вас не понимаю. Введите /help, чтобы ознакомиться с моими возможностями")

@router.message(F.content_type == ContentType.VIDEO)
async def message_video(message):
    await message.answer("Захватывающее видео, но извините, я вас не понимаю. Введите /help, чтобы ознакомиться с моими возможностями")

@router.message(F.content_type == ContentType.DOCUMENT)
async def message_document(message):
    await message.answer("Что-то интересное, но извините, я вас не понимаю. Введите /help, чтобы ознакомиться с моими возможностями")

@router.message()
async def message_other(message):
    await message.answer("Извините, но я вас не понимаю. Введите /help, чтобы ознакомиться с моими возможностями")
