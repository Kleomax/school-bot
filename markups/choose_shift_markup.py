from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ChooseStartShift = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1 смена"),
            KeyboardButton(text="2 смена")
        ]
    ],

    resize_keyboard=True
)

ChooseShift = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1 смена"),
            KeyboardButton(text="2 смена")
        ],
        [
            KeyboardButton(text="↩️ Назад")
        ]
    ],

    resize_keyboard=True
)
