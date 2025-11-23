from aiogram.filters.callback_data import CallbackData

class NavigationCallback(CallbackData, prefix="nav"):
    item_type: str
    page: int

class SelectionCallback(CallbackData, prefix="sel"):
    item_type: str
    item_id: int
