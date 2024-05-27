from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    #initial registration start state
    name = State()
    phone = State()
    birth_date = State()
    registered = State()
    # if user has entered name admin
    admin_start = State()
    admin_start_registered = State()
    # if user has entered admin password
    admin_authorized = State()
    # admin needs to enter referal code of user
    admin_referal_code = State()
    # admin need to enter how many points he wants to substract
    admin_bonus_points = State()

    admin_bonus_points_add = State()
    admin_bonus_point_sub = State()
    
    admin_message_send = State()

    admin_message_send_one = State()
    admin_message_text = State()
    admin_message_text_one = State()