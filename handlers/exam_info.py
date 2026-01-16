from aiogram import Router, F
from aiogram.types import Message, FSInputFile, ContentType
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from markups import MainMenu, ExamMenu

from database import UsersRequests

from config import ExamsInfo

router = Router()


class ExamInfo(StatesGroup):
    send_exam_info = State()


@router.message(F.text == "🎓 Расписание экзаменов")
async def choose_exam(msg: Message, state: FSMContext):
    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)
    
    if ExamsInfo == True:
        await msg.answer("Выберите тип экзамена 👇", reply_markup=ExamMenu(user_class), parse_mode=ParseMode.HTML)
        await state.set_state(ExamInfo.send_exam_info)

    else:
        await msg.answer("На данный момент расписание экзаменов неизвестно", reply_markup=MainMenu(msg.from_user.id, user_class))

    await UsersRequests.update_last_activity(user_id=msg.from_user.id)

@router.message(ExamInfo.send_exam_info)
async def send_info(msg: Message, state: FSMContext):

    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)
    
    exams = {
        "ГВЭ 9-11 классы": "ГВЭ 9-11",
        "ГИА 9 классы": "ГИА 9",
        "ГИА 11 классы": "ГИА 11"
    }

    if msg.content_type != ContentType.TEXT:
        await msg.answer('Не понимаю вас. Пожалуйста, используйте клавиатуру ниже 👇', reply_markup=ExamMenu(user_class))

    elif msg.text in exams.keys():
        await msg.answer_document(FSInputFile(f"schedules/exam_schedule/Расписание {exams.get(msg.text)}.pdf"), caption=f"Расписание {exams.get(msg.text)}", reply_markup=MainMenu(msg.from_user.id, user_class))
        await state.clear()

    elif msg.text == "↩️ Назад":
        await msg.answer('🏠 Вы вернулись в главное меню 🏠', reply_markup=MainMenu(msg.from_user.id, user_class))
        await state.clear()

    else:
        await msg.answer('Не понимаю вас. Пожалуйста, используйте клавиатуру ниже 👇', reply_markup=ExamMenu(user_class))

