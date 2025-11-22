from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Каталог")],
        [KeyboardButton(text="Корзина"), KeyboardButton(text="Контакты")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери команду",
)

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Youtube", url="https://youtube.com")],
        [InlineKeyboardButton(text="Twitch", url="https://twitch.tv")],
        [InlineKeyboardButton(text="Twitter", url="https://twitter.com")],
    ]
)