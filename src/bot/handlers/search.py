from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.states.user_states import UserStates

router = Router()

@router.callback_query(F.data == "input_city")
async def input_city(message: Message, state: FSMContext):
    await state.set_state(UserStates.waiting_for_city)
    await message.answer("Введите полное название города")

