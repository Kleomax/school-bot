from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def ChooseTheme():
    choose_theme = InlineKeyboardBuilder()

    choose_theme.row(InlineKeyboardButton(text='Вопросы по учёбе', callback_data='Вопросы по учёбе'))
    choose_theme.row(InlineKeyboardButton(text='Воспитательная работа', callback_data='Воспитательная работа'))
    choose_theme.row(InlineKeyboardButton(text='Вопросы по дневнику.pу', callback_data='Вопросы по дневнику.pу'))
    choose_theme.row(InlineKeyboardButton(text='Вопросы к директору', callback_data='Вопросы к директору'))
    choose_theme.row(InlineKeyboardButton(text='↩️ Назад', callback_data='backBtn'))

    return choose_theme.as_markup()
