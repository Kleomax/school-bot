from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from states.change_data_states import SetShiftAndClass

from markups import MainMenu, ChooseStartShift, ChooseShift, BackBtn

from database import UsersRequests

router = Router()


@router.message(Command("start"))
async def start(msg: Message, state: FSMContext):
    if not await UsersRequests.check_user_exists(msg.from_user.id):
        await UsersRequests.insert_user(user_id=msg.from_user.id)
        await UsersRequests.update_signup(user_id=msg.from_user.id, signup="SetShift")

        await msg.answer('Для начала выберите вашу смену 👇', reply_markup=ChooseStartShift)

        # Устанавливаем пользователю состояние "выбирает смену"
        await state.set_state(SetShiftAndClass.choosing_shift)
    else:
        user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)

        await msg.answer('Вы уже зарегистрированы', reply_markup=MainMenu(msg.from_user.id, user_class))

    await UsersRequests.update_last_activity(user_id=msg.from_user.id)


@router.message(F.text == '📌 Изменить смену')
async def change_shift(msg: Message, state: FSMContext):
    if await UsersRequests.check_user_exists(msg.from_user.id):
        await msg.answer('Выберите вашу смену 👇', reply_markup=ChooseShift)
        await UsersRequests.update_signup(user_id=msg.from_user.id, signup="SetShift")

        await state.set_state(SetShiftAndClass.choosing_shift)

        await UsersRequests.update_last_activity(user_id=msg.from_user.id)
    else:
        await UsersRequests.insert_user(user_id=msg.from_user.id)
        await UsersRequests.update_signup(user_id=msg.from_user.id, signup="SetShift")

        await msg.answer('Вы не зарегистрированы.\n Для начала регистрации выберите вашу смену 👇', reply_markup=ChooseStartShift)

        # Устанавливаем пользователю состояние "выбирает смену"
        await state.set_state(SetShiftAndClass.choosing_shift)


@router.message(F.text == '🖋️ Изменить класс')
async def change_class(msg: Message, state: FSMContext):
    if await UsersRequests.check_user_exists(user_id=msg.from_user.id):
        await msg.answer('Введите ваш класс ✏️\n\n<B><I>Пример: 5а</I></B>', reply_markup=BackBtn, parse_mode=ParseMode.HTML)
        
        await UsersRequests.update_signup(user_id=msg.from_user.id, signup="ChangeClass")
        await UsersRequests.update_last_activity(user_id=msg.from_user.id)

        # Устанавливаем пользователю состояние "вводит название класса"

        await state.set_state(SetShiftAndClass.change_class_name)
    else:
        await UsersRequests.insert_user(user_id=msg.from_user.id)
        await UsersRequests.update_signup(user_id=msg.from_user.id, signup="SetShift")

        await msg.answer('Вы не зарегистрированы.\n Для начала регистрации выберите вашу смену 👇', reply_markup=ChooseStartShift)

        # Устанавливаем пользователю состояние "выбирает смену"
        await state.set_state(SetShiftAndClass.choosing_shift)