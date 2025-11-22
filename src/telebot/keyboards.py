from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

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

games = ["hl1", 'hl2', 'hla']
urls = [
    "https://youtu.be/5Wavn29LMrs?si=lSK1KvETx-nTxD6-",
    "https://youtu.be/UKA7JkV51Jw?si=XlJZEzXNZghauAan",
    "https://youtu.be/O2W0N3uKXmo?si=FoXtjO16kz2Zph8Z"
]

async def inline_games():
    url_id = 0
    keyboard = InlineKeyboardBuilder()
    for game in games:
        keyboard.add(InlineKeyboardButton(text=game, url=urls[url_id]))
        url_id += 1
    return keyboard.adjust(2).as_markup()
