from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Statics = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Кол-во пользователей")
        ],
        [
            KeyboardButton(text="Кол-во вопросов за неделю")
        ]
    ],

    resize_keyboard=True
)
