import aiogram
import time

from aiogram import Router, F
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from config import bot, admins_list

from functions.mixed_fns import cancel

from markups import MainMenu, ChooseTheme, BackBtn, SkipBtn, Confirmation

from database import UsersRequests, QuestionsRequests

from states.ask import AskQuestion


router = Router()


@router.message(F.text == '\U0001F4DD Задать вопрос')
async def create_question(msg: Message, state: FSMContext):
    await msg.answer('<I>Выберите тему вопроса 👇</I>', parse_mode=ParseMode.HTML, reply_markup=ChooseTheme())

    await state.set_state(AskQuestion.get_question_theme)

    await UsersRequests.update_last_activity(user_id=msg.from_user.id)


@router.callback_query(AskQuestion.get_question_theme)
async def get_theme(call: CallbackQuery, state: FSMContext):

    user_class: str = await UsersRequests.get_class(user_id=call.from_user.id)

    if call.data == 'backBtn':
        await call.message.answer('🏠 Вы вернулись в главное меню 🏠', reply_markup=MainMenu(call.from_user.id, user_class))
        await state.clear()
    else:
        await call.message.answer('<I><B>Опишите свой вопрос</B></I> 📝', parse_mode=ParseMode.HTML, reply_markup=BackBtn)

        await state.update_data(question_theme=call.data)
        await state.set_state(AskQuestion.get_question_text)


@router.message(AskQuestion.get_question_text)
async def get_text(msg: Message, state: FSMContext):
    if msg.text == '↩️ Назад':
        await msg.answer('<I>Выберите тему вопроса 👇</I>', parse_mode=ParseMode.HTML, reply_markup=ChooseTheme())
        await state.set_state(AskQuestion.get_question_theme)

    elif msg.content_type != ContentType.TEXT:
        await msg.reply('Неверный формат. Вы можете отправить только текст', parse_mode=ParseMode.HTML)
        return

    else:
        await state.update_data(question_msg=msg.text)
        await msg.answer('<I><B>Теперь отправьте 1 фото или 1 видео</B></I> 📸', parse_mode=ParseMode.HTML, reply_markup=SkipBtn)

        await state.set_state(AskQuestion.get_question_photo)


@router.message(AskQuestion.get_question_photo)
async def get_photo(message: Message, state: FSMContext, album: list[Message] = None):

    data = await state.get_data()

    if message.text == '⏩ Пропустить':

        await message.answer(f'<I><B>Тема вопроса:</B></I> {data["question_theme"]}\n\n<I><B>Вопрос:</B></I> {data["question_msg"]}', parse_mode=ParseMode.HTML)
        await message.answer('<I><B><U>*Вопрос сформирован*</U></B></I>\n\nЧтобы его отправить, нажмите кнопку ниже👇', parse_mode=ParseMode.HTML, reply_markup=Confirmation)

        await state.update_data(question_media_group = 'None')
        await state.set_state(AskQuestion.get_confirmation)

    elif message.text == '↩️ Назад':
        await cancel(msg=message, state=state, lastState=AskQuestion.get_question_text, text='<I><B>Опишите свой вопрос</B></I> 📝', parse_mode=ParseMode.HTML, markup=BackBtn)

    elif message.content_type not in [ContentType.VIDEO, ContentType.PHOTO]:
        await message.reply('Неверный формат. Вы можете отправить только фотографии или видео')

    elif message.media_group_id != None:
        await message.reply("<I><B>Вы можете отправить только 1 фото или 1 видео</B></I> 📸", parse_mode=ParseMode.HTML, reply_markup=SkipBtn)
    # elif message.media_group_id is not None:
    #     media_group = []

    #     data = await state.get_data()

    #     if data['question_msg'] != '':
    #         media_group_build = MediaGroupBuilder(
    #             caption=f"<I><B>Тема вопроса:</B></I> {data['question_theme']}\n\n<I><B>Вопрос:</B></I> {data['question_msg']}")
    #     else:
    #         media_group_build = MediaGroupBuilder(
    #             caption=f"<I><B>Тема вопроса:</B></I> {data['question_theme']}\n\n<I>")

    #     media_number = 0

    #     for msg in album:
    #         if msg.photo:
    #             file_id = msg.photo[-1].file_id
    #             media_group.append(f"photo_{file_id}")

    #             media_group_build.add_photo(
    #                 media=file_id, parse_mode=ParseMode.HTML)

    #         elif msg.video:
    #             file_id = msg.video.file_id
    #             media_group.append(f"vid_{file_id}")

    #             media_group_build.add_video(
    #                 media=file_id, parse_mode=ParseMode.HTML)

    #         media_number += 1

    #         await state.update_data(question_media_group=media_group)

    #         await state.update_data(media_group_build=media_group_build.build())

    #         data = await state.get_data()

    #         print(media_group)
    #         print(media_group_build)

    #     await message.answer_media_group(data["media_group_build"])

    #     await message.answer('<I><B><U>*Вопрос сформирован*</U></B></I>\n\nЧтобы его отправить, нажмите кнопку ниже👇', parse_mode=ParseMode.HTML, reply_markup=Confirmation)

    #     await state.set_state(AskQuestion.get_confirmation)

    elif message.video is not None:
        await state.update_data(question_media_group=f"vid_{message.video.file_id}")

        await message.answer_video(video=message.video.file_id, caption=f"<I><B>Тема вопроса:</B></I> {data['question_theme']}\n\n<I><B>Вопрос:</B></I> {data['question_msg']}", parse_mode=ParseMode.HTML)
        await message.answer('<I><B><U>*Вопрос сформирован*</U></B></I>\n\nЧтобы его отправить, нажмите кнопку ниже👇', parse_mode=ParseMode.HTML, reply_markup=Confirmation)

        await state.set_state(AskQuestion.get_confirmation)
    
    elif message.photo is not None:
        await state.update_data(question_media_group=f"photo_{message.photo[-1].file_id}")

        await message.answer_photo(photo=message.photo[-1].file_id, caption=f"<I><B>Тема вопроса:</B></I> {data['question_theme']}\n\n<I><B>Вопрос:</B></I> {data['question_msg']}", parse_mode=ParseMode.HTML)
        await message.answer('<I><B><U>*Вопрос сформирован*</U></B></I>\n\nЧтобы его отправить, нажмите кнопку ниже👇', parse_mode=ParseMode.HTML, reply_markup=Confirmation)

        await state.set_state(AskQuestion.get_confirmation)






    # else:
    #     await state.update_data(question_photo=message.photo[-1].file_id)
    #     data = await state.get_data()

    #     await message.answer_photo(photo=data['question_photo'], caption=f"<I><B>Тема вопроса:</B></I> {data['question_theme']}\n\n<I><B>Вопрос:</B></I> {data['question_msg']}", parse_mode=ParseMode.HTML)
    #     await message.answer('<I><B><U>*Вопрос сформирован*</U></B></I>\n\nЧтобы его отправить, нажмите кнопку ниже👇', parse_mode=ParseMode.HTML, reply_markup=Confirmation)

    #     await state.set_state(AskQuestion.get_confirmation)


@router.message(AskQuestion.get_confirmation)
async def confirmation(msg: Message, state: FSMContext):

    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)

    if msg.text == '✅ Отправить':
        data = await state.get_data()

        await QuestionsRequests.add_question(
            user_id=msg.from_user.id,
            theme=data['question_theme'],
            question=data["question_msg"],
            photo=str(data['question_media_group']),
            nick=msg.from_user.full_name                                             
        )

        await msg.answer('Вопрос отправлен ✅', reply_markup=MainMenu(msg.from_user.id, user_class))

        # admins_list: list = await filter_themes(data['question_theme'])

        
        for admin in admins_list:
            try:
                await bot.send_message(chat_id=admin, text=f'🔔 <B>Появился новый вопрос 🔔</B>\n\n<I>Всего вопросов: {await QuestionsRequests.count_all_questions()}</I>', parse_mode=ParseMode.HTML)
            
            except aiogram.exceptions.TelegramForbiddenError as exc:
                print(exc)
                time.sleep(0.1)
                continue

            except aiogram.exceptions.TelegramBadRequest as exce:
                print(exce)
                time.sleep(0.1)
                continue

        await state.clear()

    elif msg.text == '❌ Отменить':
        await msg.answer('Вопрос не отправлен ❌', reply_markup=MainMenu(msg.from_user.id, user_class))
        await state.clear()

    elif msg.text == '↩️ Назад':
        await cancel(msg=msg, state=state, lastState=AskQuestion.get_question_photo, text='<I><B>Теперь отправьте 1 фото или 1 видео</B></I> 📸', markup=SkipBtn, parse_mode=ParseMode.HTML)

    elif msg.text != ContentType.TEXT:
        await msg.answer('Неверный формат. Пожалуйста, используйте клавиатуру ниже 👇', reply_markup=Confirmation)

