from aiogram.filters.callback_data import CallbackData

# Фабрика коллбэков для навигации (перемещение между страницами)
class NavigationCallback(CallbackData, prefix="nav"):
    item_type: str
    page: int

# Фабрика коллбэков для выбора университета или специальности из списка
class SelectionCallback(CallbackData, prefix="sel"):
    item_type: str
    item_id: int


