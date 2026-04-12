from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.testing.config import any_async

import src.bot.keyboards.inline as inline
import src.bot.keyboards.reply as reply
from src.bot.keyboards.callbacks import NavigationCallback, SelectionCallback, CardsCallback
from src.bot.keyboards.inline import build_pagination_keyboard
from src.bot.states.user_states import UserStates, STATES
from src.bot.keyboards.list_of_unis_and_specs import list_of_specs, list_of_unis
from src.bot.keyboards.reply import kb_back

from sqlalchemy.orm import Session
from src.database.models import  City, University, Program, SessionLocal


router = Router()


# =========================================================================
# 1. ЛОГИКА КНОПКИ "НАЗАД" (Стоит первой, чтобы перехватывать текст)
# =========================================================================

@router.message(F.text.lower() == "назад")
async def back_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()

    if current_state is None:
        return

    # СЦЕНАРИЙ 1: Мы вводили город -> Возвращаемся к выбору режима
    if current_state == UserStates.waiting_for_city:
        await state.set_state(UserStates.choosing_mode)
        await message.answer(
            "Выберите режим поиска:",
            reply_markup=inline.inline_functions  # Инлайн кнопки выбора
        )

    # СЦЕНАРИЙ 2: Мы смотрим СПИСОК (вузов или спец) -> Возвращаемся к вводу города
    elif current_state in [UserStates.selecting_uni, UserStates.selecting_spec]:
        await state.set_state(UserStates.waiting_for_city)
        # Подсказываем, какой город был введен
        saved_city = data.get("waiting_for_city", "не выбран")
        await message.answer(
            f"Текущий город: {saved_city}.\nВведите новый или нажмите кнопку выбора режима (если добавить такую кнопку).",
            reply_markup=kb_back  # Reply клавиатура
        )

    # СЦЕНАРИЙ 3: Мы провалились в КАРТОЧКУ (или список внутри вуза) -> Возвращаемся к СПИСКУ
    elif current_state == UserStates.browsing_unis_cards:
        mode = data.get("choosing_mode")

        # Если искали вузы по специальности - возвращаем список специальностей
        if mode == "Вуз по специальности":
            await state.set_state(UserStates.selecting_spec)
            await message.answer(
                "Возврат к списку специальностей:",
                reply_markup=await inline.build_pagination_keyboard(
                    items=list_of_specs,
                    page=0,
                    item_type="spec",
                )
            )
        # Если искали специальности по вузу - возвращаем список вузов
        elif mode == "Специальность по вузу":
            await state.set_state(UserStates.selecting_uni)
            await message.answer(
                "Возврат к списку вузов:",
                reply_markup=await inline.build_pagination_keyboard(
                    items=list_of_unis,
                    page=0,
                    item_type="uni",
                )
            )


# =========================================================================
# 2. ОСНОВНЫЕ ХЕНДЛЕРЫ
# =========================================================================

# Хендлер для /start (приветствие + реплай клава)
@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(UserStates.choosing_mode)
    await message.answer(
        "Привет! Я бот для поиска вузов.",
    )
    await message.answer(
        "Выберите режим поиска:",
        reply_markup=inline.inline_functions
    )


# Хендлер для выбора варианта через клаву
@router.callback_query(UserStates.choosing_mode)
async def confirm_mode(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    # Сохраняем выбор (Вуз по специальности или наоборот)
    await state.update_data(choosing_mode=callback_query.data)
    await state.set_state(UserStates.waiting_for_city)

    await callback_query.message.delete()  # Удаляем кнопки выбора режима
    await callback_query.message.answer(
        "Введите полное название города:",
        reply_markup=kb_back  # Показываем кнопку "Назад" внизу
    )


# Хендлер ввода города (Message)
@router.message(UserStates.waiting_for_city)
async def input_city(message: Message, state: FSMContext):

    if message.text not in ["Москва", "Санкт-Петербург", "Набережные Челны, Алтайский край, Мурманск"]:
        await message.answer("Город не найден в базе. Попробуйте: Москва, Санкт-Петербург")
        return

    with SessionLocal() as session:

        city_name_input = message.text.strip().capitalize()
        city = session.query(City).filter(City.full_name == city_name_input).first()

        if not city:
            await message.answer("Город не найден в базе. Попробуйте: Москва, Санкт-Петербург и т.д.")
            return

    # Сохраняем город
    await state.update_data(waiting_for_city=city.full_name, city_id=city.id)
    data = await state.get_data()
    mode = data.get("choosing_mode")

    await message.answer(f"Поиск в городе {city.full_name}...", reply_markup=kb_back)

    # Получаем режим, который выбрали ранее
    data = await state.get_data()
    mode = data.get("choosing_mode")

    await message.answer(f"Поиск в городе {message.text}...", reply_markup=kb_back)

    # Разветвление логики в зависимости от режима
    if mode == "Вуз по специальности":
        await state.set_state(UserStates.selecting_spec)
        await message.answer(
            "Выберите специальность:",
            reply_markup=await inline.build_pagination_keyboard(
                items=list_of_specs,
                page=0,
                item_type="spec",
            )
        )

    elif mode == "Специальность по вузу":
        await state.set_state(UserStates.selecting_uni)

        # Достаем все вузы для этого города из БД
        unis_in_city = session.query(University).filter(University.city_id == city.id).all()

        if not unis_in_city:
            await message.answer("В этом городе пока нет добавленных вузов.")
            return


        list_of_unis = [{"id": u.id, "name": u.name} for u in unis_in_city]
        await state.update_data(current_unis_list=list_of_unis)

        await message.answer(
            "Выберите университет:",
            reply_markup=await inline.build_pagination_keyboard(
                items=list_of_unis,
                page=0,
                item_type="uni",
            )
        )


# =========================================================================
# 3. ХЕНДЛЕРЫ НАВИГАЦИИ И ВЫБОРА
# =========================================================================

# Пагинация (листаем страницы списка)
@router.callback_query(NavigationCallback.filter(F.item_type.in_(["uni", "spec"])))
async def paginate_list(callback_query: CallbackQuery, callback_data: NavigationCallback, state: FSMContext):

    data = await state.get_data()

    if callback_data.item_type == "uni":
        current_items = data.get("current_unis_list", [])
    else:
        current_items = data.get("current_specs_list", [])

    if not current_items:
        await callback_query.answer("Данные не найдены")
        return


    keyboard = inline.build_pagination_keyboard(
        items=current_items,
        page=callback_data.page,
        item_type=callback_data.item_type,
    )

    # Редактируем сообщение (эффект листания)
    try:
        await callback_query.message.edit_reply_markup(reply_markup=await keyboard)
    except Exception:
        pass  # Игнорируем ошибку, если клавиатура не изменилась

    await callback_query.answer()


# Выбор КОНКРЕТНОГО элемента
@router.callback_query(SelectionCallback.filter())
async def select_item(callback_query: CallbackQuery, callback_data: SelectionCallback, state: FSMContext):

    await state.set_state(UserStates.browsing_unis_cards)

    item_id = int(callback_data.item_id)  # ID выбранного элемента (вуза или проги)
    item_type = callback_data.item_type

    if item_type == "uni":

        with SessionLocal() as session:
            uni = session.query(University).get(item_id)
            programs = session.query(Program).filter(Program.university_id == item_id).all()
            if not programs:
                await callback_query.answer("Для этого вуза не найдены направления.", show_alert=True)
                return

            text = f"🎓 <b>{uni.name}</b>\nДоступные направления:"

            # Превращаем объекты БД в список словарей
            # Сохраняем и название, и баллы, чтобы потом показать карточку
            list_of_specs = [
                {
                    "id": p.id,
                    "name": p.name,
                    "score": p.min_score,
                    "places": p.budget_places,
                    "subjects": p.subjects
                }
                for p in programs
            ]

            # Сохраняем в state, чтобы пагинация специальностей работала
            await state.update_data(current_specs_list=list_of_specs)

        # Выводим клавиатуру с направлениями
        await callback_query.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=await inline.build_pagination_keyboard(
                items=list_of_specs,
                page=0,
                item_type="spec",
                items_per_page=5
            )
        )

    elif item_type == "spec":
        # ПОЛЬЗОВАТЕЛЬ ВЫБРАЛ КОНКРЕТНОЕ НАПРАВЛЕНИЕ -> ПОКАЗЫВАЕМ КАРТОЧКУ (ДЕТАЛИ)
        data = await state.get_data()
        specs_list = data.get("current_specs_list", [])

        # Ищем выбранное направление в сохраненном списке по ID
        selected_spec = next((spec for spec in specs_list if spec["id"] == item_id), None)

        if selected_spec:
            text = (
                f"📚 <b>{selected_spec['name']}</b>\n\n"
                f"📊 <b>Проходной балл:</b> {selected_spec['score']}\n"
                f"👥 <b>Бюджетных мест:</b> {selected_spec['places']}\n"
                f"📝 <b>Предметы ЕГЭ:</b> {selected_spec['subjects']}"
            )
        else:
            text = "Ошибка загрузки данных о направлении."

        await callback_query.message.edit_text(
            text,
            parse_mode="HTML",

            reply_markup=await inline.build_pagination_keyboard(items=[], page=0, item_type="empty")

        )

    await callback_query.answer()
