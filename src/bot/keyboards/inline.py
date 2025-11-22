from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каталог", callback_data="catalog")],
    [InlineKeyboardButton(text="Корзина", callback_data="basket"),
     InlineKeyboardButton(text="Контакты", callback_data="contacts")],
])

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Youtube", url="https://youtube.com")],
        [InlineKeyboardButton(text="Twitch", url="https://twitch.tv")],
        [InlineKeyboardButton(text="Twitter", url="https://twitter.com")],
    ]
)
