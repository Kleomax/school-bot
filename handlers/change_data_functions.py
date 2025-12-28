import sqlite3

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType
from aiogram.enums.parse_mode import ParseMode

from states.change_data_states import SetShiftAndClass

from markups import MainMenu, ChooseStartShift, ChooseShift, BackBtn

from database import UsersRequests

from functions import get_available_classes

router = Router()

available_shift = ['1 смена', '2 смена']




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

    await UsersRequests.update_last_activity(user_id=msg.from_user.id)


@router.message(SetShiftAndClass.choosing_class_name)
async def getClass(msg: Message, state: FSMContext):

    first_shift_available_classes = await get_available_classes("first_schedule")
    second_shift_available_classes = await get_available_classes("second_schedule")

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
                available_classes = ""
                class_number = "1"

                for available_class in first_shift_available_classes:
                    if class_number != available_class[:-1]:
                        class_number = available_class[:-1]
                        available_classes += f"\n\n{available_class}       "
                    else:
                        available_classes += f"{available_class}       "

                await msg.answer(f'❗ Данного класса в 1 смене не существует. Пожалуйста, введите название класса заново\n\nДоступный список классов 1 смены:\n{available_classes}')

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

                await state.clear()
                return

        elif data['user_shift'] == '2 смена':
            if (msg.content_type != ContentType.TEXT) or (msg.text.lower() not in second_shift_available_classes):
                available_classes = ""
                class_number = "1"

                for available_class in second_shift_available_classes:
                    if class_number != available_class[:-1]:
                        class_number = available_class[:-1]
                        available_classes += f"\n\n{available_class}       "
                    else:
                        available_classes += f"{available_class}       "

                await msg.answer(f'❗ Данного класса во 2 смене не существует. Пожалуйста, введите название класса заново\n\nДоступный список классов 2 смены:\n{available_classes}')
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

                await state.clear()
                return
        else:
            await msg.answer("Ошибка на сервере. Пожалуйста, попробуйте позже")

            raise ValueError

    except TypeError:
        await msg.answer('Неверный тип данных.\nВведите название класса заново')

@router.message(SetShiftAndClass.change_class_name)
async def getClass(msg: Message, state: FSMContext):

    first_shift_available_classes = await get_available_classes("first_schedule")
    second_shift_available_classes = await get_available_classes("second_schedule")

    try:
        user_class = await UsersRequests.get_class(user_id=msg.from_user.id)

        if msg.text == '↩️ Назад':
            await msg.answer('🏠 Вы вернулись в главное меню 🏠', reply_markup=MainMenu(msg.from_user.id, user_class))
            await state.clear()

            return

        elif await UsersRequests.get_shift(user_id=msg.from_user.id) == "1 смена":
            if (msg.content_type != ContentType.TEXT) or (msg.text.lower() not in first_shift_available_classes):
                available_classes = ""
                class_number = "1"

                for available_class in first_shift_available_classes:
                    if class_number != available_class[:-1]:
                        class_number = available_class[:-1]
                        available_classes += f"\n\n{available_class}       "
                    else:
                        available_classes += f"{available_class}       "

                await msg.answer(f'❗ Данного класса в 1 смене не существует. Пожалуйста, введите название класса заново\n\nДоступный список классов 1 смены:\n{available_classes}')
                return
            
            else:
                user_class = msg.text.lower()

                await UsersRequests.update_user_class(user_id=msg.from_user.id, user_class=user_class)
                await UsersRequests.update_signup(user_id=msg.from_user.id, signup="done")
                await UsersRequests.update_activity(user_id=msg.from_user.id, activity=True)

                await msg.answer('✅ Данные успешно изменены!', reply_markup=MainMenu(msg.from_user.id, user_class))

                await state.clear()

                return

        elif await UsersRequests.get_shift(msg.from_user.id) == '2 смена':
            if (msg.content_type != ContentType.TEXT) or (msg.text.lower() not in second_shift_available_classes):
                available_classes = ""
                class_number = "1"

                for available_class in second_shift_available_classes:
                    if class_number != available_class[:-1]:
                        class_number = available_class[:-1]
                        available_classes += f"\n\n{available_class}       "
                    else:
                        available_classes += f"{available_class}       "

                await msg.answer(f'❗ Данного класса во 2 смене не существует. Пожалуйста, введите название класса заново\n\nДоступный список классов 2 смены:\n{available_classes}')
                return
            
            else:
                user_class = msg.text.lower()

                await UsersRequests.update_user_class(user_id=msg.from_user.id, user_class=user_class)
                await UsersRequests.update_signup(user_id=msg.from_user.id, signup="done")
                await UsersRequests.update_activity(user_id=msg.from_user.id, activity=True)

                await msg.answer('✅ Данные успешно изменены!', reply_markup=MainMenu(msg.from_user.id, user_class))

                await state.clear()
                return

    except TypeError:
        await msg.answer('Неверный тип данных.\nВведите название класса заново')    

    await UsersRequests.update_last_activity(user_id=msg.from_user.id)
