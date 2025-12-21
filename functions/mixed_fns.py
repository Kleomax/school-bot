import sqlite3

from aiogram.filters import BaseFilter, Filter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class IsAdmin(BaseFilter):
    def __init__(self, admins_list: list[int]) -> None:
        self.__admins_list = admins_list
    
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.__admins_list

class ChatTypeFilter(Filter):
    def __init__(self, chats: list[str]) -> None:
        self.chats = chats

    async def __call__(self, message: Message) -> bool:
        return str(message.chat.id) in self.chats


async def cancel(msg: Message, state: FSMContext, lastState, text: str, markup, parse_mode=None):
    """
    :param msg: объект Message
    :param state: объект FSMContext
    :param lastState: состояние на которое нужно вернуться
    :param text: текст сообщения
    :param markup: markup
    :param parse_mode: parse_mode (HTML, MARKDOWN)
    """


    await state.set_state(lastState)
    await msg.answer(text, parse_mode=parse_mode, reply_markup=markup)

async def get_available_classes(schedule_name: str) -> list[str]:
    """
    :param schedule_name: Название базы данных с расписание (Пример: first_schedule)
    :return: Возвращает список существующих классов (Пример: ['5а', '5б', '6а', '6б'])
    """

    connection = sqlite3.connect(f'schedules/database_schedule/{schedule_name}.sqlite3')
    cursor = connection.execute('SELECT * FROM schedule')

    shift_available_classes = [description[0]for description in cursor.description]
    shift_available_classes.remove('Звонки')

    return shift_available_classes

# async def filter_themes(theme: str) -> list: # Основной
#     if theme == 'Вопросы по учёбе':
#         return [1243852997, 1169807802]
#     elif theme == 'Воспитательная работа':
#         return [6147217410]
#     elif theme == 'Вопросы по дневнику.pу':
#         return [2028455524]
#     elif theme == 'Вопросы к директору':
#         return [5223960363]
    

# async def filter_themes(theme: str) -> list: # Для тестов
#     if theme == 'Вопросы по учёбе':
#         return [8144024776]
#     elif theme == 'Воспитательная работа':
#         return [5773470793]
#     elif theme == 'Вопросы по дневнику.pу':
#         return [1224172892]
#     elif theme == 'Вопросы к директору':
#         return [1224172892]



# @router.message(Sender.get_photo)
# async def get_keyboard(msg: Message, state: FSMContext):
#     if msg.text == '\U000021A9 Назад':
#         await state.set_state(Sender.get_text)
#         await msg.answer('Введите текст рассылки')
#         return
#     elif msg.text != '\U000023E9 Пропустить':
#         try:
#             print(msg.media_group_id)
#             # await bot.copy_message(chat_id=msg.from_user.id, message_id=msg.media_group_id)

#             # while msg.photo[-1].file_id:
#             # for msg_photo in await state.update_data(msg_photo = msg.photo[-1].file_id):
#             # i = 0
#             # d = []
#             # for i in range(5):
#             #     # d["group" + str(i)] = msg.photo[-1].file_id
#             #     d += msg.photo[-1].file_id
                

#             # await state.update_data(msg_photo_1 = msg.photo[-1].file_id)
#             # while i < 5:
#             # await state.update_data(gdfjgdljgdjgdjg = d)
#             #     i += 1
#             # data = await state.get_data()
#         except TypeError:
#             await msg.answer('Неверный формат')
#             return
#     # else:
#     #     data = await state.get_data()
#     #     if data['msg_text'] != '':
#     #         await state.update_data(msg_photo = '')
#     #     else:
#     #         await msg.answer('\U000026A0 Вы ничего не ввели. Рассылка отменена', reply_markup=main_markup.Admin())
#     #         await state.clear()
#     #         return
#     # # await msg.answer('Введите текст для кнопки')
#     # # await state.set_state(Sender.get_keyboard)
