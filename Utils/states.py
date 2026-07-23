from aiogram.fsm.state import State, StatesGroup

class PersonState(StatesGroup):
    waiting_for_name = State()
    chatting = State()


