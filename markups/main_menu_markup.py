from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import admins_list


def MainMenu(user_id: int, user_class: str):
    keyboard_btns = [
        [
            KeyboardButton(text="📚 Расписание")
        ],
        [
            KeyboardButton(text="📝 Задать вопрос")
        ],
        [
            KeyboardButton(text="📌 Изменить смену"),
            KeyboardButton(text="🖋️ Изменить класс"),
        ],
        [
            KeyboardButton(text="📖 Помощь с домашней работой 📖")
        ],
        [
            KeyboardButton(text="📥 Скачать расписание")
        ],
        [
            KeyboardButton(text="💡 Предложить идею")
        ]
    ]

    if user_class.startswith("9") or user_class.startswith("11"):
        keyboard_btns.insert(2, [KeyboardButton(text="🎓 Расписание экзаменов")])

    if user_id in admins_list:
        keyboard_btns.insert(0, [KeyboardButton(text="🗂️ Вопросы")])
        keyboard_btns.insert(2, [KeyboardButton(text="📨 Отправить рассылку")])
        keyboard_btns.insert(7, [KeyboardButton(text="📊 Статистика")])
        keyboard_btns.insert(6, [KeyboardButton(text="🚫 Список заблокированных")])

        keyboard_btns.remove([KeyboardButton(text='📝 Задать вопрос')])

    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard_btns,
        resize_keyboard=True,
    )

    return keyboard