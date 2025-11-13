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

@router.message(ExamInfo.send_exam_info)
async def send_info(msg: Message, state: FSMContext):

    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)

    if msg.content_type != ContentType.TEXT:
        await msg.answer('Не понимаю вас. Пожалуйста, используйте клавиатуру ниже 👇', reply_markup=ExamMenu(user_class))
    
    elif msg.text == "ГВЭ 9-11 классы":
        await msg.answer_document(FSInputFile("schedules/exam_schedule/Расписание ГВЭ 9-11.pdf"), caption="Расписание ГВЭ 9-11", reply_markup=MainMenu(msg.from_user.id, user_class))
        await state.clear()

    elif msg.text == "ГИА 9 классы":
        await msg.answer_document(FSInputFile("schedules/exam_schedule/Расписание ГИА 9.pdf"), caption="Расписание ГИА 9", reply_markup=MainMenu(msg.from_user.id, user_class))
        await state.clear()

    elif msg.text == "ГИА 11 классы":
        await msg.answer_document(FSInputFile("schedules/exam_schedule/Расписание ГИА 11.pdf"), caption="Расписание ГИА 11", reply_markup=MainMenu(msg.from_user.id, user_class))
        await state.clear()

    elif msg.text == "↩ Назад":
        await msg.answer('🏠 Вы вернулись в главное меню 🏠', reply_markup=MainMenu(msg.from_user.id, user_class))
        await state.clear()

    else:
        await msg.answer('Не понимаю вас. Пожалуйста, используйте клавиатуру ниже 👇', reply_markup=ExamMenu(user_class))
