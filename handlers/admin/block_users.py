from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.fsm.state import StatesGroup, State

from functions.mixed_fns import IsAdmin, cancel

from config import admins_list, bot

from markups import BlockedUsers, MainMenu, BlockUser

from database import UsersRequests  


router = Router()


class Unblock(StatesGroup):
    get_confirm = State()


@router.message(F.text == "🚫 Список заблокированных")
async def get_blocked_users(msg: Message):

    blocked_users = await UsersRequests.get_all_blocked_users()

    if len(blocked_users) != 0:
        await msg.answer("Выберите пользователя 👇", reply_markup=BlockedUsers(blocked_users))
    else:
        await msg.answer("Список заблокированных пользователей пуст")

@router.callback_query(F.data.startswith("unblock_"))
async def unblock_user(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f"Вы уверены, что хотите разблокировать пользователя <i><b>{call.data.split('unblock_')[1]}</b></i>?", parse_mode=ParseMode.HTML, reply_markup=BlockUser)

    await state.update_data(user = call.data.split("unblock_")[1])
    await state.set_state(Unblock.get_confirm)

@router.message(Unblock.get_confirm)
async def get_unblock_confirm(msg: Message, state: FSMContext):

    user_class = await UsersRequests.get_class(user_id=msg.from_user.id)

    data = await state.get_data()
    user = data["user"]

    if msg.text == "✅ Да":
        try:
            await bot.send_message(user, "Вы были разблокированы! Теперь вы можете пользоваться ботом 😌", reply_markup=MainMenu(user, user_class))
            await msg.answer(f"Пользователь {user} успешно разблокирован ✅", reply_markup=MainMenu(msg.from_user.id, user_class))
            
            await UsersRequests.unblock_user(user_id=int(user), activity="active")

        except (TelegramBadRequest, TelegramForbiddenError):
            await msg.answer(f"Пользователь {user} успешно разблокирован ✅, но он заблокировал бота, либо же его аккаунт был удалён", reply_markup=MainMenu(msg.from_user.id, user_class))
            
            await UsersRequests.unblock_user(user_id=int(user), activity="inactive")

        await state.clear()

    elif msg.text == "❌ Нет":
        await msg.answer(f"Разблокировка пользователя {user} отменена ❌", reply_markup=MainMenu(msg.from_user.id, user_class))

        await state.clear()
