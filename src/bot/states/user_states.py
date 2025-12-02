from aiogram.fsm.state import StatesGroup, State


# FSM-состояния
class UserStates(StatesGroup):
    choosing_mode = State()
    waiting_for_city = State()
    selecting_uni = State()
    selecting_spec = State()
    browsing_unis_or_specs = State()
    browsing_unis_cards = State()
    reading_reviews = State()