from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from markups import MainMenu, BackBtn

from functions.idea_fn import send_email

from database import UsersRequests

router = Router()

class get_idea(StatesGroup):
    wait_idea = State()

@router.message(F.text == "💡 Предложить идею")
async def idea_btn(msg: Message, state: FSMContext):
    await msg.answer("📋 Напишите, чтобы вы хотели видеть нового в данном боте", reply_markup=BackBtn)
    
    await state.set_state(get_idea.wait_idea)

    await UsersRequests.update_last_activity(user_id=msg.from_user.id)

@router.message(get_idea.wait_idea)
async def idea(msg: Message, state: FSMContext):

    user_class: str = await UsersRequests.get_class(user_id=msg.from_user.id)

    if msg.text == "↩️ Назад":
        await msg.answer('🏠 Вы вернулись в главное меню 🏠', reply_markup=MainMenu(msg.from_user.id, user_class))
        await state.clear()

    elif len(msg.text) > 10:
        login = "telegram.bot.ideas@gmail.com"
        password = "mncocrmakvlawjte" 

        subject = "Новая идея для бота"
        recipient_mail = "daniilbelkin8@gmail.com"
        input = f"User_id: {msg.from_user.id}\nUser_name: {msg.from_user.full_name}\nUser_nick: {msg.from_user.username}\n\nИдея: {msg.text}"

        await msg.answer('Отправляем вашу идею, пожалуйста подождите 📨')

        try:
            send_email(login, password, subject, recipient_mail, input)
            
            await msg.answer('Идея успешно отправлена разработчику ✅', reply_markup=MainMenu(msg.from_user.id, user_class))

        except ConnectionError:
            await msg.answer('Произошла ошибка на сервере. К сожалению, ваша идея не отправлена 😔', reply_markup=MainMenu(msg.from_user.id, user_class))
        
        finally:
            await state.clear()
    
    else:
        await msg.answer("⚠️ Слишком маленькое описание идеи. Пожалуйста, опишите её по подробнее", reply_markup=BackBtn)
