
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤖 ИИ 🤖", callback_data="gpt")],
        [InlineKeyboardButton(text="🎲 Рандомный факт 🎲", callback_data="fact")],
        [InlineKeyboardButton(text="👤 Общение с Персонажем 👤", callback_data="person")],
        [InlineKeyboardButton(text="ℹ️ О боте ℹ️", callback_data="about")]],

    )

def gpt_exit_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Выйти из GPT",
                    callback_data="exit_gpt"
                )
            ]
        ]
    )

def person_exit_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Завершить общение",
                    callback_data="exit_person"
                )
            ]
        ]
    )
