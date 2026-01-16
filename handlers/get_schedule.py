import sqlite3

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode

from markups import MainMenu

from database import UsersRequests

router = Router()


@router.message(F.text == "📚 Расписание")
async def get(msg: Message):
    user_shift = await UsersRequests.get_shift(user_id=msg.from_user.id)
    user_class = await UsersRequests.get_class(user_id=msg.from_user.id)


    if user_shift == '1 смена':
        con = sqlite3.connect('schedules/database_schedule/first_schedule.sqlite3')
        cur = con.cursor()
    elif user_shift == '2 смена':
        con = sqlite3.connect('schedules/database_schedule/second_schedule.sqlite3')
        cur = con.cursor()

    try:
        cur.execute(f'SELECT Звонки, [{user_class}] FROM schedule')
        table = cur.fetchall()

        info = ''
        lesson = ""
        lesson_time = ""
        day_of_week = 1

        for el in table:
            if el[1] is not None and el[1] != ' ':
                
                if el[0] != None:
                    lesson_time = el[0]
                else:
                    lesson_time = ""

                if el[1] == user_class:
                    day_of_week += 1

                    if day_of_week == 2:
                        lesson = f"{'-' * 21} ( Вторник ) {'-' * 21}" # максимум 56 символов
                    elif day_of_week == 3:
                        lesson = f"{'-' * 22} ( Среда ) {'-' * 22}"
                    elif day_of_week == 4:
                        lesson = f"{'-' * 21} ( Четверг ) {'-' * 21}"
                    elif day_of_week == 5:
                        lesson = f"{'-' * 21} ( Пятница ) {'-' * 21}"
                else:
                    lesson = el[1]

                info += f'{lesson_time} {lesson}\n\n'

        await msg.answer(f'<b><U>📚 Расписание {user_class}</U></b>\n\n {"-" * 17} ( Понедельник ) {"-" * 17}\n\n{info}',
                         parse_mode=ParseMode.HTML)
        
    except sqlite3.OperationalError:
        await msg.answer(f'Расписание для {user_class} не найдено. Проверьте смену и класс',
                          reply_markup=MainMenu(msg.from_user.id, user_class))
    
    cur.close()
    con.close()

    await UsersRequests.update_last_activity(user_id=msg.from_user.id)

@router.message(F.text == "📥 Скачать расписание")
async def download_schedule(msg: Message):

    user_shift: str = await UsersRequests.get_shift(user_id=msg.from_user.id)

    if user_shift == '1 смена':
        schedule = 'schedules/image_schedule/first-schedule-image.png'

    elif user_shift == '2 смена':
        schedule = 'schedules/image_schedule/second-schedule-image.png'

    user_shift = user_shift.replace('а', 'ы')

    await msg.answer_document(document=FSInputFile(path=schedule, filename='Расписание.png'), caption=f'Расписание {user_shift}')

    await UsersRequests.update_last_activity(user_id=msg.from_user.id)
    
