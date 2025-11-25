from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder
from src.bot.keyboards.callbacks import NavigationCallback, SelectionCallback


inline_functions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Вуз по специальности", callback_data="Вуз по специальности")],
    [InlineKeyboardButton(text="Специальность по вузу", callback_data="Специальность по вузу")],
])


async def build_pagination_keyboard(items: list, page: int, item_type: str, items_per_page: int = 5):
    builder = InlineKeyboardBuilder() # Объект класса InlineKeyboardBuilder

    # Задаём промежутки для отображения items_per_page страниц
    start_index = page * items_per_page
    end_index = start_index + items_per_page
    current_page_items = items[start_index:end_index]

    # Добавляем кнопки в builder
    for item in current_page_items:
        builder.button(
            text=item["title"],
            callback_data=SelectionCallback(item_type=item_type, item_id=item["id"]),
        )

    builder.adjust(1)

    nav_buttons = []

    # Создание кнопки "влево"
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="◀️",
                callback_data=NavigationCallback(item_type=item_type, page=page - 1).pack()
            )
        )

    # Создание счётчика страниц
    total_pages = (len(items) + items_per_page - 1) // items_per_page
    nav_buttons.append(
        InlineKeyboardButton(
            text=f"{page + 1}/️{total_pages}",
            callback_data="noop",
        )
    )

    # Создание кнопки "вправо"
    if end_index < len(items):
        nav_buttons.append(
            InlineKeyboardButton(
                text="▶️",
                callback_data=NavigationCallback(item_type=item_type, page=page + 1).pack()
            )
        )

    # Добавление нижних кнопок в builder
    builder.row(*nav_buttons)

    return builder.as_markup()

