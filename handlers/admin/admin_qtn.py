from aiogram import Router
from aiogram.types import Message, ContentType, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from functions.mixed_fns import IsAdmin, cancel
from functions.get_questions import get_question

from config import admins_list, bot

from states.qtn_system_states import AnswerQuestion

from markups import MainMenu, BackBtn, BlockUser, CreateReply, SkipBtn, Confirmation

from database import UsersRequests, QuestionsRequests

router = Router()


router.message.filter(IsAdmin(admins_list))


@router.message(AnswerQuestion.start)
async def write_answer(msg: Message, state: FSMContext):

    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)

    if msg.text== '↩️ Назад':
        await msg.answer('🏠 Вы вернулись в главное меню 🏠', reply_markup=MainMenu(msg.from_user.id, user_class))

        await state.clear()
    
    elif msg.text == '📝 Ответить':
        await msg.answer('Для начала введите ответ пользователю в виде текста 📝', reply_markup=BackBtn)
        await state.set_state(AnswerQuestion.get_admin_answer)
    
    elif msg.text == '🚫 Заблокировать пользователя':
        await msg.answer("Вы уверены, что хотите заблокировать пользователя?", reply_markup=BlockUser)
        await state.set_state(AnswerQuestion.block_user)

    else:
        await msg.answer('Не понимаю вас. Пожалуйста, используйте клавиатуру ниже👇', reply_markup=CreateReply)


@router.message(AnswerQuestion.block_user)
async def block_user(msg: Message, state: FSMContext):

    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)

    if msg.text == "✅ Да":

        data = await state.get_data()

        await UsersRequests.block_user(data["user_id"])
        await UsersRequests.update_activity(data["user_id"], False)
        await QuestionsRequests.delete_question(int(data['user_id']), theme=data['theme'], qtn=data['qtn'], photo=data['media'])

        await bot.send_message(data["user_id"], "К сожалению, вы были заблокированы. С этого момента вы не сможете пользоваться данным ботом 😔", reply_markup=ReplyKeyboardRemove())

        await msg.answer("Пользователь был успешно заблокирован ✅")
        await msg.answer(f"Осталось вопросов: {await QuestionsRequests.count_all_questions()}", reply_markup=MainMenu(msg.from_user.id, user_class))

        await state.clear()
    
    elif msg.text == "❌ Нет":
        await state.clear()

        await msg.answer("Блокировка отменена ❌")

        all_questions: list = await QuestionsRequests.get_all_questions()

        await get_question(all_questions, state, msg)


@router.message(AnswerQuestion.get_admin_answer) 
async def send_answer(msg: Message, state: FSMContext):

    user_class = await UsersRequests.get_class(user_id=msg.from_user.id)

    if msg.content_type != ContentType.TEXT:
        await msg.reply('Неверный формат. Вы можете отправить только текст')
        return
    
    elif msg.text == '↩️ Назад':
        await msg.answer('🏠 Вы вернулись в главное меню 🏠', reply_markup=MainMenu(msg.from_user.id, user_class))
        await state.clear()
    
    else:
        await state.update_data(admin_answer = msg.text)

        await msg.answer('Теперь отправьте 1 фото или 1 видео 🖼', reply_markup=SkipBtn)
        
        await state.set_state(AnswerQuestion.get_admin_photo)


@router.message(AnswerQuestion.get_admin_photo)
async def send_photo(msg: Message, state: FSMContext):
    data = await state.get_data() 

    if msg.text == '⏩ Пропустить':
        await state.update_data(admin_media = 'None')

        await msg.answer(data['admin_answer'])
        await msg.answer('<I><U>*Ответ сформирован*</U></I>\n\nЧтобы его отправить, нажмите кнопку ниже', parse_mode=ParseMode.HTML, reply_markup=Confirmation)
        
        await state.set_state(AnswerQuestion.get_confirmation)
    
    elif msg.text == '↩️ Назад':
        await msg.answer('Введите ответ пользователю в виде текста 📝', reply_markup=BackBtn)
        await state.set_state(AnswerQuestion.get_admin_answer)
    
    elif msg.content_type not in [ContentType.PHOTO, ContentType.VIDEO]:
        await msg.reply('Неверный формат. Вы можете отправить только фото или видео')
    
    elif msg.media_group_id is not None:
        await msg.reply('Вы можете отправить только 1 фотографию или 1 видео')
    
    else:
        if msg.content_type == ContentType.PHOTO:
            await state.update_data(admin_media = f"photo_{msg.photo[-1].file_id}")
            await msg.answer_photo(photo = msg.photo[-1].file_id, caption=data['admin_answer'])
            
        elif msg.content_type == ContentType.VIDEO:
            await state.update_data(admin_media = f"vid_{msg.video.file_id}")
            await msg.answer_video(video = msg.video.file_id, caption=data['admin_answer'])

        await msg.answer('<I><U>*Ответ сформирован*</U></I>\n\nЧтобы его отправить, нажмите кнопку ниже', parse_mode=ParseMode.HTML, reply_markup=Confirmation)
        
        await state.set_state(AnswerQuestion.get_confirmation)


@router.message(AnswerQuestion.get_confirmation)
async def get_answer_confirmation(msg: Message, state: FSMContext):

    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)

    if msg.text == '✅ Отправить':
        data = await state.get_data()

        user_media: str = data["media"]
        admin_media: str = data["admin_media"]

        try:

            if data['admin_answer'] != 'None':
                if user_media != 'None':
                    if user_media.startswith("photo_"):
                        await bot.send_photo(chat_id=int(data['user_id']), photo=user_media.replace("photo_", ""), caption=f'<I><B>Тема вопроса:</B></I> {data["theme"]}\n\n<I><B>Вопрос:</B></I> {data["qtn"]} \n\n<I><U><B>На ваш вопрос ответили:👇</B></U></I>',
                                            parse_mode=ParseMode.HTML)
                    elif user_media.startswith("vid_"):
                        await bot.send_video(chat_id=int(data['user_id']), video=user_media.replace("vid_", ""), caption=f'<I><B>Тема вопроса:</B></I> {data["theme"]}\n\n<I><B>Вопрос:</B></I> {data["qtn"]} \n\n<I><U><B>На ваш вопрос ответили:👇</B></U></I>',
                                                parse_mode=ParseMode.HTML)
                else:
                    await bot.send_message(chat_id=int(data['user_id']), text=f'<I><B>Тема вопроса:</B></I> {data["theme"]}\n\n<I><B>Вопрос:</B></I> {data["qtn"]} \n\n<I><U><B>На ваш вопрос ответили:👇</B></U></I>', parse_mode=ParseMode.HTML)
                
                if admin_media != 'None':
                    if admin_media.startswith("photo_"):
                        await bot.send_photo(chat_id=int(data['user_id']), photo=data['admin_media'].replace("photo_", ""), caption=data['admin_answer'])
                    else:
                        await bot.send_video(chat_id=int(data["user_id"]), video=data['admin_media'].replace("vid_", ""), caption=data['admin_answer'])
                else:
                    await bot.send_message(chat_id=int(data['user_id']), text=data['admin_answer'])

                await msg.answer('✅ Пользователь получил ваш ответ', reply_markup=MainMenu(msg.from_user.id, user_class))
            else:
                await msg.answer('Вы ничего не ввели. Ответ не отправлен', reply_markup=MainMenu(msg.from_user.id, user_class))

        except TelegramForbiddenError:
            await msg.answer('Пользователь заблокировал бота или удалил аккаунт. Вопрос был удалён из базы данных', reply_markup=MainMenu(msg.from_user.id, user_class))
        
        except TelegramBadRequest:
            await msg.answer('Чат с пользователем не найден. Вопрос был удалён из базы данных', reply_markup=MainMenu(msg.from_user.id, user_class))
        
        finally:

            await state.clear()

            await QuestionsRequests.delete_question(user_id=int(data['user_id']), theme=data['theme'], qtn=data['qtn'], photo=user_media)

            await msg.answer(f"Осталось вопросов: {await QuestionsRequests.count_all_questions()}")

            await state.clear()

    elif msg.text == '❌ Отменить':
        await msg.answer('Ответ не отправлен', reply_markup=MainMenu(msg.from_user.id, user_class))
        await state.clear()
    
    elif msg.text == '↩️ Назад':
        await cancel(msg=msg, state=state, lastState=AnswerQuestion.get_admin_photo, text='Теперь отправьте 1 фото или 1 видео 🖼', markup=SkipBtn, parse_mode=ParseMode.HTML)
    
    elif msg.text != ContentType.TEXT:
        await msg.answer('Неверный формат. Пожалуйста, используйте клавиатуру ниже👇', reply_markup=Confirmation)
