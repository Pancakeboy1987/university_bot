from aiogram.fsm.state import StatesGroup, State

class UserStates(StatesGroup):
    choosing_mode = State()
    waiting_for_city = State()
    selecting_uni = State()
    selecting_spec = State()
    browsing_carousel = State()
    reading_reviews = State()