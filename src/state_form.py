from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    #initial registration start state
    name = State()
    phone = State()
    birth_date = State()
    registered = State()