from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from functions.questions_system_test import QuestionSystem
from functions.mixed_fns import IsAdmin
from functions.get_questions import get_question

from states.qtn_system_states import AnswerQuestion


QuestionsSys = QuestionSystem()


import asyncio
asyncio.run(QuestionsSys.initialize())

router = Router()


router.message.filter(IsAdmin([1224172892]))

theme = 'Вопросы по дневнику.pу'


@router.message(F.text == '\U0001F5C2 Вопросы')
async def next_question(msg: Message, state: FSMContext):
    all_questions = await QuestionsSys.get_all_questions_by_theme(theme=theme)

    await get_question(all_questions, state, msg)


@router.message(AnswerQuestion.count_questions)
async def count_questions(msg: Message, state: FSMContext):
    await msg.answer(f'<I>Осталось вопросов: {len(QuestionsSys.get_all_questions_by_theme(theme=theme))}</I>', parse_mode=ParseMode.HTML)

    await state.clear()
