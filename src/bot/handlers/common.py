from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import src.bot.keyboards.inline as inline
from src.bot.keyboards.callbacks import NavigationCallback, SelectionCallback
from src.bot.keyboards.inline import build_pagination_keyboard
from src.bot.states.user_states import UserStates
from src.bot.keyboards.list_of_unis_and_specs import list_of_specs, list_of_unis

router = Router()

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.set_state(UserStates.choosing_mode)
    await message.answer(
        "Выберите один из вариантов:",
        reply_markup=inline.inline_functions
    )

@router.callback_query(UserStates.choosing_mode)
async def input_city(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data(choosing_mode=callback_query.data)
    await state.set_state(UserStates.waiting_for_city)
    await callback_query.message.edit_text("Введите полное название города")

@router.message(UserStates.waiting_for_city)
async def input_city(message: Message, state: FSMContext):
    if message.text in ["Москва", "Санкт-Петербург", "Набережные Челны"]:
        await state.update_data(waiting_for_city=message.text)
    else:
        await message.answer("Вы ввели неправильные данные\nПопробуйте ещё раз")
        return
    data = await state.get_data()
    if data["choosing_mode"] == "Вуз по специальности":
        await state.set_state(UserStates.selecting_spec)
        await message.answer(
            "Выберите специальность:",
            reply_markup=await inline.build_pagination_keyboard(
                items=list_of_specs,
                page=0,
                item_type="spec"
            )
        )
    elif data["choosing_mode"] == "Специальность по вузу":
        await state.set_state(UserStates.selecting_uni)
        await message.answer(
            "Выберите университет:",
            reply_markup=await inline.build_pagination_keyboard(
                items=list_of_unis,
                page=0,
                item_type="uni"
            )
        )

@router.callback_query(NavigationCallback.filter(F.item_type.in_(["uni", "spec"])))
async def paginate_unis_of_specs(callback_query: CallbackQuery, callback_data: NavigationCallback, state: FSMContext):
    data_source = {
        "spec": list_of_specs,
        "uni": list_of_unis,
    }

    current_items = data_source[callback_data.item_type]
    if not current_items:
        await callback_query.answer("Ошибка: данные не найдены")
        return

    keyboard = build_pagination_keyboard(
        items=current_items,
        page=callback_data.page,
        item_type=callback_data.item_type,
    )

    try:
        await callback_query.message.edit_reply_markup(reply_markup=await keyboard)
    except Exception:
        pass

    await callback_query.answer()

@router.callback_query(SelectionCallback.filter(F.item_type.in_(["uni", "spec"])))
async def uni_or_specs_selected(callback_query: CallbackQuery, callback_data: SelectionCallback, state: FSMContext):
    pass

