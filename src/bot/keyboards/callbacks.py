from aiogram.filters.callback_data import CallbackData

# Для навигации (перемещение между страницами)
class NavigationCallback(CallbackData, prefix="nav"):
    item_type: str
    page: int

# Для выбора университета или специальности из списка
class SelectionCallback(CallbackData, prefix="sel"):
    item_type: str
    item_id: int


