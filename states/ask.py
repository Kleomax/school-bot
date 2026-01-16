from aiogram.fsm.state import StatesGroup, State

class AskQuestion(StatesGroup):
    get_question_theme = State()
    get_question_text = State()
    get_question_photo = State()
    ready = State()
    get_confirmation = State()
