from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

# Тестовая реплай клава
reply_test = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Помощь"), KeyboardButton(text="Предыдущий шаг"), KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
)