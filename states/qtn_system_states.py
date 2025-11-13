from aiogram.fsm.state import StatesGroup, State

class AnswerQuestion(StatesGroup):
    start = State()
    get_admin_answer = State()
    get_admin_photo = State()
    get_confirmation = State()
    count_questions = State()
    block_user = State()
