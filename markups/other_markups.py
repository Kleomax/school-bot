from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

BackBtn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="↩️ Назад")
        ]
    ],

    resize_keyboard=True,
    one_time_keyboard=True
)

SkipBtn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⏩ Пропустить")
        ],
        [
            KeyboardButton(text="↩️ Назад")
        ],
    ],

    resize_keyboard=True
)


def InlineBtn(text: str, url: str):
    btn = InlineKeyboardBuilder()
    btn.row(InlineKeyboardButton(text=text, url=url))

    return btn.as_markup()

def ExampleBtn():
    btn = InlineKeyboardBuilder()
    btn.row(InlineKeyboardButton(text='Пример', url='https://www.google.ru/'))

    return btn.as_markup()

def DeleteMailing():
    btn = InlineKeyboardBuilder()
    btn.row(InlineKeyboardButton(text='❌ Удалить последнюю рассылку', callback_data='delete_mailing'))

    return btn.as_markup()

def UnblockUser(blocked_users: list[int]):
    users = InlineKeyboardBuilder()

    for user in blocked_users:
        users.row(InlineKeyboardButton(text=str(user), callback_data=f"unblock_{user}"))

    return users.as_markup()
