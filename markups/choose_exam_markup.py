from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def ExamMenu(user_class: str):
    keyboard_btns = [
        [
            KeyboardButton(text="↩️ Назад"),
        ],
    ]

    exams = [KeyboardButton(text="ГВЭ 9-11 классы")]

    if user_class.startswith("9"):
        exams.insert(0, KeyboardButton(text="ГИА 9 классы"))
    elif user_class.startswith("11"):
        exams.insert(0, KeyboardButton(text="ГИА 11 классы"))

    keyboard_btns.insert(0, exams)


    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard_btns,
        resize_keyboard=True,
        input_field_placeholder='Воспользуйтесь меню:'
    )

    return keyboard
