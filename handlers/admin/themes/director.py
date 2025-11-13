from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from functions.questions_system_test import QuestionSystem
from functions.mixed_fns import IsAdmin
from functions.get_questions import get_question

from states.qtn_system_states import AnswerQuestion

QuestionsSys = QuestionSystem()
router = Router()


router.message.filter(IsAdmin([5223960363]))

theme = 'Вопросы к директору'


@router.message(F.text == '\U0001F5C2 Вопросы')
async def next_question(msg: Message, state: FSMContext):
    all_questions = QuestionsSys.get_all_questions_by_theme(theme=theme)
    
    await get_question(all_questions, state, msg)

@router.message(AnswerQuestion.count_questions)
async def count_questions(msg: Message, state: FSMContext):
    await msg.answer(f'Осталось вопросов: {len(QuestionsSys.get_all_questions_by_theme(theme=theme))}')

    await state.clear()
