from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import src.bot.keyboards.inline as inline


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет, это тестовая версия бота.\nВот что я предлагаю:",
    reply_markup=inline.inline_functions,
    )

