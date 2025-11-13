import sqlite3

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType
from aiogram.enums.parse_mode import ParseMode

from states.change_data_states import SetShiftAndClass

from markups import MainMenu, ChooseStartShift, ChooseShift, BackBtn

from database import UsersRequests


router = Router()

available_shift = ['1 смена', '2 смена']

first_connection = sqlite3.connect('schedules/database_schedule/first_schedule.sqlite3')
first_cursor = first_connection.execute('SELECT * FROM schedule')

first_shift_available_classes = [description[0] for description in first_cursor.description]
first_shift_available_classes.remove('Звонки')


second_connection = sqlite3.connect('schedules/database_schedule/second_schedule.sqlite3')
second_cursor = second_connection.execute('SELECT * FROM schedule')

second_shift_available_classes = [description[0] for description in second_cursor.description]
second_shift_available_classes.remove('Звонки')



@router.message(SetShiftAndClass.choosing_shift)
async def getShift(msg: Message, state: FSMContext):

    if msg.text == '↩️ Назад' and (await UsersRequests.get_shift(msg.from_user.id) != 'None' and await UsersRequests.get_class(msg.from_user.id) != 'None'):
        user_class = await UsersRequests.get_class(user_id=msg.from_user.id)
        
        await msg.answer('🏠 Вы вернулись в главное меню 🏠', reply_markup=MainMenu(msg.from_user.id, user_class))
        await state.clear()

        return
    
    elif (msg.content_type != ContentType.TEXT) or (msg.text.lower() not in available_shift):
        if await UsersRequests.get_shift(user_id=msg.from_user.id) == "None" and await UsersRequests.get_class(user_id=msg.from_user.id) == "None":
            await msg.answer('❗Данной смены не существует. Пожалуйста, выберите смену используя клавиатуру ниже', reply_markup=ChooseStartShift)
        else:
            await msg.answer('❗Данной смены не существует. Пожалуйста, выберите смену используя клавиатуру ниже', reply_markup=ChooseShift)
    
    else:
        await state.update_data(user_shift = msg.text.lower())

        await UsersRequests.update_signup(user_id=msg.from_user.id, signup="SetClass")

        if msg.text.lower() == '1 смена':
            await msg.answer('Введите ваш класс ✏️\n\n<B><I>Пример: 5а</I></B>', reply_markup=BackBtn, parse_mode=ParseMode.HTML)
        else:
            await msg.answer('Введите ваш класс ✏️\n\n<B><I>Пример: 6а</I></B>', reply_markup=BackBtn, parse_mode=ParseMode.HTML)
        
        await state.set_state(SetShiftAndClass.choosing_class_name)

@router.message(SetShiftAndClass.choosing_class_name)
async def getClass(msg: Message, state: FSMContext):
    
    try:
        data = await state.get_data()

        if msg.text == '↩️ Назад':
            if await UsersRequests.get_class(user_id=msg.from_user.id) != "None":
                await msg.answer('Выберите вашу смену 👇', reply_markup=ChooseShift)
            else:
                await msg.answer('Выберите вашу смену 👇', reply_markup=ChooseStartShift)

            await state.set_state(SetShiftAndClass.choosing_shift)

            return

        elif data['user_shift'] == '1 смена':
            if (msg.content_type != ContentType.TEXT) or (msg.text.lower() not in first_shift_available_classes):
                await msg.answer('❗ Данного класса в 1 смене не существует. Пожалуйста, введите название класса заново')
                
                return
            
            else:
                user_class = msg.text.lower()

                if user_class != 'None':
                    await msg.answer('✅ Данные успешно изменены', reply_markup=MainMenu(msg.from_user.id, user_class))
                else:
                    await msg.answer('✅ Регистрация прошла успешно!', reply_markup=MainMenu(msg.from_user.id, user_class))

                await UsersRequests.update_user_shift(user_id=msg.from_user.id, user_shift=data["user_shift"])
                await UsersRequests.update_user_class(user_id=msg.from_user.id, user_class=user_class)
                await UsersRequests.update_signup(user_id=msg.from_user.id, signup="done")
                await UsersRequests.unblock_user(user_id=msg.from_user.id, activity="active")

                await state.clear()
                return

        elif data['user_shift'] == '2 смена':
            if (msg.content_type != ContentType.TEXT) or (msg.text.lower() not in second_shift_available_classes):
                await msg.answer('❗ Данного класса во 2 смене не существует. Пожалуйста, введите название класса заново')
                return
            
            else:
                user_class = msg.text.lower()

                if user_class != 'None':
                    await msg.answer('✅ Данные успешно изменены', reply_markup=MainMenu(msg.from_user.id, user_class))
                else:
                    await msg.answer('✅ Регистрация прошла успешно!', reply_markup=MainMenu(msg.from_user.id, user_class))

                await UsersRequests.update_user_shift(user_id=msg.from_user.id, user_shift=data["user_shift"])
                await UsersRequests.update_user_class(user_id=msg.from_user.id, user_class=user_class)
                await UsersRequests.update_signup(user_id=msg.from_user.id, signup="done")
                await UsersRequests.unblock_user(user_id=msg.from_user.id, activity="active")

                await state.clear()
                return

    except TypeError:
        await msg.answer('Неверный тип данных.\nВведите название класса заново')

@router.message(SetShiftAndClass.change_class_name)
async def getClass(msg: Message, state: FSMContext):
    try:

        user_class = await UsersRequests.get_class(user_id=msg.from_user.id)

        if msg.text == '↩️ Назад':
            await msg.answer('🏠 Вы вернулись в главное меню 🏠', reply_markup=MainMenu(msg.from_user.id, user_class))
            await state.clear()

            return

        elif await UsersRequests.get_shift(user_id=msg.from_user.id) == "1 смена":
            if (msg.content_type != ContentType.TEXT) or (msg.text.lower() not in first_shift_available_classes):
                await msg.answer('❗ Данного класса в 1 смене не существует. Пожалуйста, введите название класса заново')
                return
            
            else:
                user_class = msg.text.lower()

                await UsersRequests.update_user_class(user_id=msg.from_user.id, user_class=user_class)
                await UsersRequests.update_signup(user_id=msg.from_user.id, signup="done")
                await UsersRequests.update_activity(user_id=msg.from_user.id, activity="active")

                await msg.answer('✅ Данные успешно изменены!', reply_markup=MainMenu(msg.from_user.id, user_class))

                await state.clear()

                return

        elif await UsersRequests.get_shift(msg.from_user.id) == '2 смена':
            if (msg.content_type != ContentType.TEXT) or (msg.text.lower() not in second_shift_available_classes):
                await msg.answer('❗ Данного класса во 2 смене не существует. Пожалуйста, введите название класса заново')
                return
            
            else:
                user_class = msg.text.lower()

                await UsersRequests.update_user_class(user_id=msg.from_user.id, user_class=user_class)
                await UsersRequests.update_signup(user_id=msg.from_user.id, signup="done")
                await UsersRequests.update_activity(user_id=msg.from_user.id, activity="active")

                await msg.answer('✅ Данные успешно изменены!', reply_markup=MainMenu(msg.from_user.id, user_class))

                await state.clear()
                return

    except TypeError:
        await msg.answer('Неверный тип данных.\nВведите название класса заново')        
