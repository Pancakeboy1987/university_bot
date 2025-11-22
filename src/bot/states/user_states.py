from aiogram.fsm.state import StatesGroup, State

class UserStates(StatesGroup):
    waiting_for_city = State()
    choosing_mode = State()
    selecting_uni = State()
    selecting_spec = State()
    browsing_carousel = State()
    reading_reviews = State()

