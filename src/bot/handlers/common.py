import random

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import src.bot.keyboards.inline as kb


class Reg(StatesGroup):
    name = State()
    phone_number = State()


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text="Холла!",
        reply_markup=kb.main,
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

@router.callback_query(F.data == "catalog")
async def get_catalog(callback: CallbackQuery):
    parts = [str(random.randint(0, 255)) for _ in range(4)]
    await callback.message.edit_text(
        f"Твой IP: {".".join(parts)}",
        reply_markup=kb.main
    )

@router.message(Command("reg"))
async def reg(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer("Введите своё имя")


@router.message(Reg.name)
async def get_user_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.phone_number)
    await message.answer("Введите номер телефона")

@router.message(Reg.phone_number)
async def get_user_phone(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    answer = await message.answer(
        f"Регистрация завершена"
        f"\nИмя: {data["name"]}"
        f"\nНомер телефона: {data["phone_number"]}"
    )
    await state.clear()

