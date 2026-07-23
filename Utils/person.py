from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Utils.states import PersonState
from Utils.gpt import client

router = Router()

user_person = {}


# 🔘 кнопка выхода
def exit_person_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Выйти из персонажа", callback_data="exit_person")]
    ])


# --- Нажали кнопку ---
@router.callback_query(lambda c: c.data == "person")
async def choose_person(callback: CallbackQuery, state: FSMContext):
    await state.clear()  # 🔥 важно
    await callback.message.answer("👤 Напиши имя личности (например: Илон Маск)")
    await state.set_state(PersonState.waiting_for_name)
    await callback.answer()


# --- Ввод имени ---
@router.message(PersonState.waiting_for_name)
async def set_person(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    person_name = message.text

    user_person[user_id] = person_name

    await message.answer(f"Гримируюсь в {person_name}...💅")

    # 🔥 СРАЗУ ответ от персонажа
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": f"Ты {person_name}. Представься и поприветствуй пользователя в своём стиле."
            }
        ],
    )

    answer = response.choices[0].message.content

    await message.answer(answer, reply_markup=exit_person_kb())

    await state.set_state(PersonState.chatting)


# --- Общение ---
@router.message(PersonState.chatting)
async def chat_as_person(message: types.Message):
    user_id = message.from_user.id
    person_name = user_person.get(user_id, "известная личность")

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"Ты {person_name}. Отвечай как этот человек. Если этот человек в публичном поле использовал матные слова, "
                               f"то тоже можешь их использовать, но не переборщи"
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ],
        )

        answer = response.choices[0].message.content
        await message.answer(answer, reply_markup=exit_person_kb())

    except Exception as e:
        print("GPT error:", e)
        await message.answer("Ошибка 😢")


# --- Выход ---
@router.callback_query(lambda c: c.data == "exit_person")
async def exit_person(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Ты вышел из режима персонажа")
    await callback.answer()