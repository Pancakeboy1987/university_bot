import random

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text="Холла!",
        reply_markup=await kb.inline_games(),
    )

@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("помощи не жди, трудяга "
                         "- кабзда тебе от бешеной бродяги")

@router.message(F.text == "Когда выйдет ХЛ 3?")
async def get_hlx(message: Message):
    await message.answer(f"HL3 выйдет через {random.randint(5, 15)} лет")

@router.message(F.photo)
async def get_photo(message: Message):
    await message.reply(f"ID фото: {message.photo[-1].file_id}")

@router.message(Command("get_photo"))
async def get_photo(message: Message):
    await message.answer_photo(
        photo="AgACAgIAAxkBAAMdaR_XcBDuLw9zJkFnwiH4JWKcyNIAAuQNaxsyhgABSQh0rTLU_StXAQADAgADbQADNgQ",
        caption="СКИН НА МАИНКРАВТ СКАЧАТЬ ПРОНА ХХХ 365"
    )

