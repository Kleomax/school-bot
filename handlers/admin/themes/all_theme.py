from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from functions.mixed_fns import IsAdmin
from functions.get_questions import get_question


from database import QuestionsRequests

router = Router()


router.message.filter(IsAdmin([1224172892, 2028455524]))


@router.message(F.text == "🗂️ Вопросы")
async def next_question(msg: Message, state: FSMContext):

    all_questions: list = await QuestionsRequests.get_all_questions()

    await get_question(all_questions, state, msg)

