from aiogram import Router, F
from aiogram.types import Message

from functions.mixed_fns import IsAdmin

from config import admins_list

from database import UsersRequests

router = Router()

router.message.filter(IsAdmin(admins_list))


@router.message(F.text == "📊 Статистика")
async def get_statics(msg: Message):
    all_users: int = await UsersRequests.count_all_users()
    activity_users: int = await UsersRequests.get_all_active_users()

    await msg.answer(f"Общее кол-во пользователей: {all_users}\nКол-во активных пользователей: {activity_users}")