from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from openai import OpenAI
from os import getenv
from dotenv import load_dotenv
from collections import defaultdict, deque
from Utils.keyboard import gpt_exit_keyboard
from aiogram.filters import StateFilter

router = Router()

load_dotenv()
client = OpenAI(api_key=getenv("API_KEY"))

# 👉 Храним пользователей в режиме GPT
gpt_users = set()
user_memory = defaultdict(lambda: deque(maxlen=15))


# --- ВКЛЮЧЕНИЕ GPT ---
def enable_gpt(user_id):
    gpt_users.add(user_id)


# --- ВЫКЛЮЧЕНИЕ GPT ---
def disable_gpt(user_id):
    gpt_users.discard(user_id)


# --- ОБРАБОТКА СООБЩЕНИЙ ---
@router.message(StateFilter(None))
async def chat(message: types.Message):
    user_id = message.from_user.id

    # если GPT выключен — игнорируем
    if user_id not in gpt_users:
        return

    await message.answer("Дай ка мне подумать...🤔")

    try:

        # добавляем вопрос пользователя в память
        user_memory[user_id].append(
            {
                "role": "user",
                "content": message.text
            }
        )

        messages = [
            {
                "role": "system",
                "content": "Отвечай кратко, понятно. Учитывай предыдущие сообщения."
            }
        ]

        # добавляем историю
        messages.extend(user_memory[user_id])

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages,
        )

        answer = response.choices[0].message.content

        # сохраняем ответ GPT
        user_memory[user_id].append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        await message.answer(
            answer,
        reply_markup=gpt_exit_keyboard()),





    except Exception as e:
        print("OpenAI error:", e)
        await message.answer("Ошибка GPT 😢")


