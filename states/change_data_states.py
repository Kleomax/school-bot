from aiogram.fsm.state import StatesGroup, State

class SetShiftAndClass(StatesGroup):
    choosing_shift = State()
    choosing_class_name = State()
    change_class_name = State()
