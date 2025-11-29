from aiogram.filters.callback_data import CallbackData

# Фабрика коллбэков для навигации при выборе университета/специальности из списка
class NavigationCallback(CallbackData, prefix="nav"):
    item_type: str
    page: int

# Фабрика коллбэков для выбора университета/специальности из списка
class SelectionCallback(CallbackData, prefix="sel"):
    item_type: str
    item_id: int

class CardsCallback(CallbackData, prefix="cards"):
    item_type: str
    page: int

