from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

inline_functions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Вуз по специальности", callback_data="input_city")],
    [InlineKeyboardButton(text="Специальность по вузу", callback_data="input_city")],
])