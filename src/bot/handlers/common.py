from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import src.bot.keyboards.inline as inline
from src.bot.keyboards.callbacks import NavigationCallback, SelectionCallback, CardsCallback
from src.bot.keyboards.inline import build_pagination_keyboard
from src.bot.states.user_states import UserStates
from src.bot.keyboards.list_of_unis_and_specs import list_of_specs, list_of_unis

router = Router()

# Хендлер для "/start"
@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.set_state(UserStates.choosing_mode) # Обращение к 1-му стейту юзера
    await message.answer(
        "Выберите один из вариантов:",
        reply_markup=inline.inline_functions
    )


# Хендлер для выбора варианта через клаву
@router.callback_query(UserStates.choosing_mode)
async def input_city(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data(choosing_mode=callback_query.data) # Дата полученная с инлайна
    await state.set_state(UserStates.waiting_for_city)
    await callback_query.message.edit_text("Введите полное название города")


# Хендлер для ввода города
@router.message(UserStates.waiting_for_city)
async def input_city(message: Message, state: FSMContext):

    # Проверка на корректность ввода города
    if message.text in ["Москва", "Санкт-Петербург", "Набережные Челны"]:
        await state.update_data(waiting_for_city=message.text)
    else:
        await message.answer("Вы ввели неправильные данные\nПопробуйте ещё раз")
        return

    data = await state.get_data()   # Получаем данные по состояниям

    # Вывод определённой клавиатуры (зависит от выбора режима при "/start")
    if data["choosing_mode"] == "Вуз по специальности":
        await state.set_state(UserStates.selecting_spec)
        await message.answer(
            "Выберите специальность:",
            reply_markup=await inline.build_pagination_keyboard(
                items=list_of_specs,
                page=0,
                item_type="spec",
            )
        )
    elif data["choosing_mode"] == "Специальность по вузу":
        await state.set_state(UserStates.selecting_uni)
        await message.answer(
            "Выберите университет:",
            reply_markup=await inline.build_pagination_keyboard(
                items=list_of_unis,
                page=0,
                item_type="uni",
            )
        )


# Хендлер для пагинации
@router.callback_query(NavigationCallback.filter(F.item_type.in_(["uni", "spec"])))
async def paginate_unis_of_specs(callback_query: CallbackQuery, callback_data: NavigationCallback, state: FSMContext):

    # Получаем данные по уникам/специальностям из списков (потом адаптировать под БД)
    data_source = {
        "spec": list_of_specs,
        "uni": list_of_unis,
    }
    if callback_query.data == "spec":
        await state.update_data(selecting_spec=callback_query.data)
    else:
        await state.update_data(selecting_uni=callback_query.data)


    # Проверка на то, что данные правильно считались
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


# noinspection PyTypeChecker
# Хендлер для вывода карточек (пока без карточек)
@router.callback_query(SelectionCallback.filter(F.item_type == "spec"))
async def specs_of_uni(callback_query: CallbackQuery, callback_data: SelectionCallback, state: FSMContext):
    await callback_query.answer()
    await state.set_state(UserStates.browsing_carousel)

    spec_id = callback_data.item_id
    await callback_query.message.edit_text(
        f"Вы выбрали специальность: {spec_id}",
        reply_markup=await inline.build_pagination_keyboard(
            items=list_of_unis,
            page=0,
            item_type="spec",
            items_per_page=1
        )
    )


# noinspection PyTypeChecker
@router.callback_query(CardsCallback.filter(F.item_type == "spec"))
async def unis_carousel(callback_query: CallbackQuery, callback_data: CardsCallback, state: FSMContext):
    await state.update_data()

    keyboard = build_pagination_keyboard(
        items=list_of_unis,
        page=callback_data.page,
        item_type=callback_data.item_type,
        items_per_page=1
    )

    try:
        await callback_query.message.edit_reply_markup(reply_markup=await keyboard)
    except Exception:
        pass

    await callback_query.answer()