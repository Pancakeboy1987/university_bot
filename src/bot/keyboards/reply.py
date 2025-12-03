from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

# Тестовая реплай клава
reply_test = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)