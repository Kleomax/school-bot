from aiogram import Router
from aiogram.types import Message

from markups import main_menu_markup

from database import UsersRequests

router = Router()


@router.message()
async def any(msg: Message):
    user_class = await UsersRequests.get_class(user_id=msg.from_user.id)

    await msg.answer('Не понимаю вас. Пожалуйста, используйте клавиатуру ниже 👇', reply_markup=main_menu_markup.MainMenu(msg.from_user.id, user_class))
