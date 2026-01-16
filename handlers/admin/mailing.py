import asyncio
import time
import fontstyle

from aiogram import Router, F
from aiogram.types import Message, ContentType, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest, TelegramRetryAfter

from config import bot, admins_list

from middleware import SomeMiddleware

from functions import mixed_fns

from markups import MainMenu, SkipBtn, BackBtn, ExampleBtn, Confirmation, InlineBtn, DeleteMailing

from database import UsersRequests


router = Router()

router.message.filter(mixed_fns.IsAdmin(admins_list))

class Sender(StatesGroup):
    get_text = State()
    get_photo = State()
    get_keyboard = State()
    get_url = State()
    get_confirmation = State()
    confirmation = State()


@router.message(F.text == '📨 Отправить рассылку')
async def get_text(msg: Message, state: FSMContext):
    await msg.answer('<I>*Создание рассылки*</I>\n\nНиже отправьте текст рассылки', reply_markup=SkipBtn, parse_mode=ParseMode.HTML)
    await state.set_state(Sender.get_text)

    await UsersRequests.update_last_activity(user_id=msg.from_user.id)

@router.message(Sender.get_text)
async def get_photo(msg: Message, state: FSMContext):

    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)

    if msg.content_type != ContentType.TEXT:
        await msg.answer('Неверный формат. Пожалуйста, введите текст или используйте клавиатуру ниже👇', reply_markup=SkipBtn)
        return
    else:
        if msg.text == '↩️ Назад':
            await state.clear()
            await msg.answer('🏠 Вы вернулись в главное меню 🏠', reply_markup=MainMenu(msg.from_user.id, user_class))
            
            return
        
        elif msg.text != '⏩ Пропустить':
            await state.update_data(msg_text = msg.text)
        
        else:
            await state.update_data(msg_text = '')
        
        await msg.answer('Теперь отправьте до 10 фотографий или видео', reply_markup=SkipBtn)
        await state.set_state(Sender.get_photo)


router.message.middleware(SomeMiddleware())
@router.message(Sender.get_photo)
async def handle_albums(message: Message, state: FSMContext, album: list[Message] = None):

    user_class: str = await UsersRequests.get_class(user_id=message.from_user.id)

    try:
        if message.text == '↩️ Назад':
            await mixed_fns.cancel(msg=message, state=state, lastState=Sender.get_text, text='Введите текст рассылки', markup=SkipBtn)
            return
        
        elif message.text == '⏩ Пропустить':
            data = await state.get_data()

            if data['msg_text'] != '':
                await state.update_data(media_group = '')

                await message.answer('Введите текст для кнопки', reply_markup=SkipBtn)
                
                await message.answer('<I>Пример такой кнопки👇</I>', parse_mode=ParseMode.HTML, reply_markup=ExampleBtn())
                await state.set_state(Sender.get_keyboard)
            
            else:
                await message.answer('❌ Вы ничего не ввели. Рассылка отменена', reply_markup=MainMenu(message.from_user.id, user_class))
                await state.clear()
                
                return
        
        elif message.media_group_id is not None:
            data = await state.get_data()
            media_group = MediaGroupBuilder(caption=f"<I>Последние новости школы 👀</I>\n\n{data['msg_text']}")
            
            media_number = 0

            for msg in album:
                if msg.photo:
                    file_id = msg.photo[-1].file_id
                    media_group.add_photo(media=file_id, parse_mode=ParseMode.HTML)

                elif msg.video:
                    file_id = msg.video.file_id
                    media_group.add_video(media=file_id, parse_mode=ParseMode.HTML)
    
                media_number += 1

                await state.update_data(media_group=media_group.build())
                data = await state.get_data()

            await state.update_data(media_number = media_number)

            if data['msg_text'] != '':
                await message.answer_media_group(data['media_group'])
            else: 
                await message.answer_media_group(media=data['media_group'])

            await message.answer('*Сообщение для рассылки сформировано*\n\nЧтобы начать, нажмите кнопку ниже', reply_markup=Confirmation)
            await state.set_state(Sender.confirmation)
            
        else:

            if message.video is not None:
                await state.update_data(media_group = f"vid_{message.video.file_id}")

            else:
                await state.update_data(media_group = f"photo_{message.photo[-1].file_id}")

            await message.answer('Введите текст для кнопки', parse_mode=ParseMode.HTML, reply_markup=SkipBtn)
            await message.answer('<I>Пример такой кнопки👇</I>', parse_mode=ParseMode.HTML, reply_markup=ExampleBtn())
            
            await state.set_state(Sender.get_keyboard)
            
    except TypeError as ex:
        await message.reply('Неверный формат', reply_markup=SkipBtn)
        print(ex)


@router.message(Sender.get_keyboard)
async def get_keyboard_url(msg: Message, state: FSMContext):
    if msg.content_type != ContentType.TEXT:
        await msg.answer('Неверный формат. Пожалуйста введите текст или используйте клавиатуру ниже👇', reply_markup=SkipBtn)
        
        return
    else:
        
        if msg.text == '↩️ Назад':
            await mixed_fns.cancel(msg=msg, state=state, lastState=Sender.get_photo, text='Отправьте до 10 фотографий или видео', markup=SkipBtn)
            return
        
        elif msg.text != '⏩ Пропустить':
            await state.update_data(btn_text = msg.text)

            await msg.answer('Введите ссылку для кнопки\n\n<I>Пример: https://www.google.ru</I>', reply_markup=BackBtn, parse_mode=ParseMode.HTML)
            
            await state.set_state(Sender.get_url)
        
        else:
            await state.update_data(btn_text = '')

            data = await state.get_data()

            if data['media_group'] != '':
                if len(data['media_group']) < 15:
                    if data['msg_text'] != '':
                        await msg.answer_media_group(data['media_group'])
                    else:
                        await msg.answer_media_group(data['media_group'])
                else:

                    if data['media_group'].startswith("vid_"):
                        await msg.answer_video(caption=data['msg_text'], video=data['media_group'].replace("vid_", ""))
                    else:
                        await msg.answer_photo(caption=data['msg_text'], photo=data['media_group'].replace("photo_", ""))
            else:
                await msg.answer(text=data['msg_text'])
                
            await msg.answer('<I><U>*Сообщение для рассылки сформировано*</U></I>\n\nЧтобы начать, нажмите кнопку ниже 👇',
                            reply_markup=Confirmation,
                            parse_mode=ParseMode.HTML)
            
            await state.set_state(Sender.confirmation)


@router.message(Sender.get_url)
async def get_confirmation(msg: Message, state: FSMContext):

    if msg.content_type != ContentType.TEXT:
        await msg.answer('Неверный формат. Пожалуйста введите текст или используйте клавиатуру ниже👇', reply_markup=BackBtn)
        
        return
    
    else:
        if msg.text == '↩️ Назад':
            await mixed_fns.cancel(msg=msg, state=state, lastState=Sender.get_keyboard, text='Введите текст для кнопки', markup=SkipBtn)
            
            return
        
        await state.update_data(btn_url = msg.text)
        
        data = await state.get_data()

        try: 
            if data['media_group'] != '':
                if len(data['media_group']) < 15:
                    if data['msg_text'] != '':
                        await msg.answer_media_group(data['media_group'])     
                
                else:
                    if data['media_group'].startswith("vid_"):
                        await msg.answer_video(caption=data['msg_text'], video=data['media_group'].replace("vid_", ""), reply_markup=InlineBtn(text=data['btn_text'], url=data['btn_url']))
                    else:
                        await msg.answer_photo(caption=data['msg_text'], photo=data['media_group'].replace("photo_", ""), reply_markup=InlineBtn(text=data['btn_text'], url=data['btn_url']))
            else:
                await msg.answer(data['msg_text'], reply_markup=InlineBtn(text=data['btn_text'], url=data['btn_url']))
        
        except TelegramBadRequest:
            await msg.answer('<U>Это не ссылка</U>', parse_mode=ParseMode.HTML, reply_markup=BackBtn)
            
            return
        
        await msg.answer('<I><U>*Сообщение для рассылки сформировано*</U></I>\n\nЧтобы начать, нажмите кнопку ниже 👇',
                        reply_markup=Confirmation,
                        parse_mode=ParseMode.HTML)
        
        await state.set_state(Sender.confirmation)



@router.message(Sender.confirmation, F.text == '✅ Отправить')
async def start_mailing(msg: Message, state: FSMContext):
    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)
    user_list: list[int] = await UsersRequests.get_all_users_id()

    await msg.answer('<I>Начал рассылку, ожидайте её завершения...</I>', parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()

    successful_msgs = 0
    msgs = []

    for user in user_list:
        try:
            if data['media_group'] != '':
                if len(data['media_group']) > 15:
                    if data['btn_text'] != '':
                        if data['media_group'].startswith("vid_"):
                            message = await bot.send_video(chat_id=user, caption=f"<I>Последние новости школы 👀</I>\n\n{data['msg_text']}", parse_mode=ParseMode.HTML, video=data['media_group'].replace("vid_", ""), reply_markup=InlineBtn(text=data['btn_text'], url=data['btn_url']))
                        else:
                            message = await bot.send_photo(chat_id=user, caption=f"<I>Последние новости школы 👀</I>\n\n{data['msg_text']}", parse_mode=ParseMode.HTML, photo=data['media_group'].replace("photo_", ""), reply_markup=InlineBtn(text=data['btn_text'], url=data['btn_url']))

                        msgs += f"{message.message_id}/"
                    
                    else:
                        if data['media_group'].startswith("vid_"):
                            message = await bot.send_video(chat_id=user, caption=f"<I>Последние новости школы 👀</I>\n\n{data['msg_text']}", parse_mode=ParseMode.HTML, video=data['media_group'].replace("vid_", ""))
                        else:
                            message = await bot.send_photo(chat_id=user, caption=f"<I>Последние новости школы 👀</I>\n\n{data['msg_text']}", parse_mode=ParseMode.HTML, photo=data['media_group'].replace("photo_", ""))
                        msgs += f"{message.message_id}/"
                
                elif len(data['media_group']) < 15:
                    message = await bot.send_media_group(chat_id=user, media=list(data['media_group']))

                    for i in range(data['media_number']):
                        msgs += f"{message[i].message_id}/"
            else:
                if data['btn_text'] != '':
                    message = await bot.send_message(chat_id=user, text=f"<I>Последние новости школы 👀</I>\n\n{data['msg_text']}", parse_mode=ParseMode.HTML, reply_markup=InlineBtn(text=data['btn_text'], url=data['btn_url']))
                    msgs += f"{message.message_id}/"
                else:
                    message = await bot.send_message(chat_id=user, text=f"<I>Последние новости школы 👀</I>\n\n{data['msg_text']}", parse_mode=ParseMode.HTML)
                    msgs += f"{message.message_id}/"

            await UsersRequests.update_activity(user_id=user, activity=True)

            successful_msgs += 1

        except TelegramForbiddenError as exc:
            print(fontstyle.apply(exc, 'bold/Italic/yellow'))

            await UsersRequests.update_activity(user_id=user, activity=False)

            time.sleep(0.1)
            continue

        except TelegramBadRequest as exce:
            print(fontstyle.apply(exce, 'bold/Italic/yellow'))

            await UsersRequests.update_activity(user_id=user, activity=False)

            time.sleep(0.1)
            continue

        except TelegramRetryAfter as ex:
            print(fontstyle.apply(f"Rate limit, wait {ex.retry_after} seconds", 'bold/Italic/yellow'))
            
            await asyncio.sleep(ex.retry_after)
            
            return await start_mailing(msg, state)
        
    message_ids = ''

    for i in msgs:
        message_ids += i

    message_ids = message_ids.split('/')
    message_ids = list(filter(None, message_ids))


    print(fontstyle.apply(f'[+] Кол-во отправленных сообщений: {successful_msgs}/{len(user_list)}', 'bold/Italic/green'))
    
    await msg.answer('✅ Сообщения отправлены!', reply_markup=MainMenu(msg.from_user.id, user_class))
    await msg.answer(f'<I>[+] Кол-во отправленных сообщений: {successful_msgs}/{len(user_list)}</I>', parse_mode=ParseMode.HTML, reply_markup=DeleteMailing())
    
    for admin in admins_list:
        if admin != msg.from_user.id:
            await bot.send_message(chat_id=admin, text=f'<I>[+] Кол-во отправленных сообщений: {successful_msgs}/{len(user_list)}</I>', parse_mode=ParseMode.HTML)


    await state.clear()
    await state.update_data(messages = message_ids)


@router.message(Sender.confirmation, F.text == '\U0000274C Отменить')
async def stop_mailing(msg: Message, state: FSMContext):
    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)

    await msg.answer('❌ Рассылка отменена', reply_markup=MainMenu(msg.from_user.id, user_class))
    await state.clear()


@router.message(Sender.confirmation, F.text == '↩️ Назад')
async def BackBtn(msg: Message, state: FSMContext):
    data = await state.get_data()

    if data['media_group'] != '':
        if len(data['media_group']) > 15:    
            await mixed_fns.cancel(msg=msg, state=state, lastState=Sender.get_keyboard, text='Введите текст для кнопки', markup=SkipBtn)
        else:
            await mixed_fns.cancel(msg=msg, state=state, lastState=Sender.get_photo, text='Отправьте до 10 фотографий или видео',markup=SkipBtn)
    else:
        await mixed_fns.cancel(msg=msg, state=state, lastState=Sender.get_keyboard, text='Введите текст для кнопки', markup=SkipBtn)
    

@router.callback_query(F.data == 'delete_mailing')
async def delete_mailing(call: CallbackQuery, state: FSMContext):

    user_list = await UsersRequests.get_all_users_id() 

    data = await state.get_data()

    await call.message.answer('<I>Начал удаление рассылки, ожидайте её завершения...</I>', parse_mode=ParseMode.HTML)

    for user in user_list:
        try:
            await bot.delete_messages(chat_id=user, message_ids=data['messages'])
        
        except TelegramForbiddenError as exc:
            print(fontstyle.apply(exc, 'bold/Italic/yellow'))
            asyncio.sleep(0.2)

            continue
        
        except TelegramBadRequest as exce:
            print(fontstyle.apply(exce, 'bold/Italic/yellow'))
            asyncio.sleep(0.2)

            continue
        
        except TelegramRetryAfter as ex:
            print(fontstyle.apply(f"Rate limit, wait {ex.retry_after} seconds", 'bold/Italic/yellow'))
            
            await asyncio.sleep(ex.retry_after)

            return await delete_mailing(call, state)

    await call.message.answer('✅ Рассылка успешно удалена')

    await state.clear()

    await UsersRequests.update_last_activity(user_id=call.from_user.id)
