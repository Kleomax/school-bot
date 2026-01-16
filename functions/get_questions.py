from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.qtn_system_states import AnswerQuestion

from markups import MainMenu, CreateReply

from database import UsersRequests, QuestionsRequests


async def get_question(all_questions: list[list], state: FSMContext, msg: Message):

    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)

    if all_questions:
        await state.set_state(AnswerQuestion.start)

        user_id: int = int(all_questions[0])
        theme: str = all_questions[1]
        question: str = all_questions[2]
        media: str = all_questions[3]
        nick: str = all_questions[4]

        await state.update_data(user_id=user_id)
        await state.update_data(theme=theme)
        await state.update_data(qtn=question)
        await state.update_data(media=media)


        if media.startswith("photo_"):
            await msg.answer_photo(photo=media.replace("photo_", ""), caption=f'<I>Вопрос от <a href="tg://user?id={user_id}">{nick}</a>:</I>\nUser_id: {user_id}\n\n<I><B>Тема вопроса:</B> {theme}</I>\n\n<I><B>Вопрос:</B> {question}</I>',
                                parse_mode=ParseMode.HTML,
                                reply_markup=CreateReply)
        elif media.startswith("vid_"):
            await msg.answer_video(video=media.replace("vid_", ""), caption=f'<I>Вопрос от <a href="tg://user?id={user_id}">{nick}</a>:</I>\nUser_id: {user_id}\n\n<I><B>Тема вопроса:</B> {theme}</I>\n\n<I><B>Вопрос:</B> {question}</I>',
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=CreateReply)
        else:
            await msg.answer(f'<I>Вопрос от <a href="tg://user?id={user_id}">{nick}</a>:</I>\nUser_id: {user_id}\n\n<I><B>Тема вопроса:</B> {theme}</I>\n\n<I><B>Вопрос:</B> {question}</I>',
                            parse_mode=ParseMode.HTML,
                            reply_markup=CreateReply)

        await msg.answer(f'<I>Всего вопросов: {await QuestionsRequests.count_all_questions()}</I>', parse_mode=ParseMode.HTML)

    else:
        await msg.answer('Вопросы закончились', reply_markup=MainMenu(msg.from_user.id, user_class))
