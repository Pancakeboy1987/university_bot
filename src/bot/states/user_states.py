from aiogram.fsm.state import StatesGroup, State

from src.bot import states


# FSM-состояния
class UserStates(StatesGroup):
    choosing_mode = State()
    waiting_for_city = State()
    selecting_uni = State()
    selecting_spec = State()
    browsing_unis_or_specs = State()
    browsing_unis_cards = State()
    reading_reviews = State()

STATES = [
    UserStates.choosing_mode,
    UserStates.waiting_for_city,
    UserStates.selecting_uni,
    UserStates.selecting_spec,
    UserStates.browsing_unis_or_specs,
    UserStates.browsing_unis_cards,
    UserStates.reading_reviews
]