from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

CreateReply = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Ответить")
        ],
        [
            KeyboardButton(text="↩️ Назад")
        ],
        [
            KeyboardButton(text="🚫 Заблокировать пользователя")
        ]
    ],

    resize_keyboard=True
)

BlockUser = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Да")
        ],
        [
            KeyboardButton(text="❌ Нет")
        ]
    ],

    resize_keyboard=True
)

Confirmation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Отправить"),
            KeyboardButton(text="❌ Отменить")
        ],
        [
            KeyboardButton(text='↩️ Назад')
        ]
    ],
    
    one_time_keyboard=True,
    resize_keyboard=True
)
