from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

reply_test = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Помощь"), KeyboardButton(text="Предыдущий шаг"), KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
)