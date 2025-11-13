from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


from database import UsersRequests

from markups import BackBtn, MainMenu

from functions import request_ai

from states import HomeworkQuestion

from config import API_KEYS

router = Router()


@router.message(F.text == "📖 Помощь с домашней работой 📖")
async def change_role(msg: Message, state: FSMContext):

    await msg.answer("Введите свой вопрос по домашней работе и нейросеть даст подсказку по её решению", parse_mode="HTML", reply_markup=BackBtn)

    await state.set_state(HomeworkQuestion.get_question)


@router.message(HomeworkQuestion.get_question, F.text == "↩️ Назад")
async def back(msg: Message, state: FSMContext):
    user_class = await UsersRequests.get_class(user_id=msg.from_user.id)

    await msg.answer("🏠 Вы вернулись в главное меню 🏠", reply_markup=MainMenu(user_id=msg.from_user.id, user_class=user_class))

    await state.clear()


@router.message(HomeworkQuestion.get_question, F.text)
async def request_prompt(msg: Message):
    await msg.answer("Вопрос отправлен! Ожидайте ответа...", reply_markup=ReplyKeyboardRemove())

    prompt = msg.text.strip()

    for index, api_key in enumerate(API_KEYS, start=1):
        json_data = await request_ai(api_key=api_key, prompt=prompt)

        if json_data != False:
            with open("key_info.txt", "+w", encoding="UTF-8") as file:
                file.write(f"Рабочий токен - {index}\n\n{api_key}")
                
            break

    ai_answer: str = json_data['choices'][0]['message']['content'].replace("*", "")
    
    ai_answer = ai_answer.split("</think>")

    if len(ai_answer) == 3:
        ai_answer = ai_answer[2]
    elif len(ai_answer) == 2:
        ai_answer = ai_answer[1]

    # prompt_tokens = json_data['usage']["prompt_tokens"]
    # completion_tokens = json_data['usage']['completion_tokens']
    total_tokens = json_data['usage']['total_tokens']


    if len(ai_answer) > 4096:
        for x in range(0, len(ai_answer), 4096):
            await msg.answer(f"{ai_answer[x:x+4096]}", parse_mode=None, reply_markup=BackBtn)
    else:
        await msg.answer(f"{ai_answer}", parse_mode=None, reply_markup=BackBtn)

