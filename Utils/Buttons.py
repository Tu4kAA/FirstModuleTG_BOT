from aiogram import Router, types
from Utils.bot_description import bot_about
from Utils.gpt import enable_gpt
from Utils.gpt import disable_gpt
from Utils.gpt import client
router = Router()


@router.callback_query(lambda c: c.data == "gpt")
async def gpt_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    enable_gpt(user_id)

    await callback.message.answer("/gpt")
    await callback.message.answer_photo(
        photo="https://surl.li/jnkljs",  # ссылка на картинку
        caption="🤖 ИИ готов к работе! Напиши свой вопрос"
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "exit_gpt")
async def exit_gpt(callback: types.CallbackQuery):
    disable_gpt(callback.from_user.id)

    await callback.message.answer("GPT выключен ❌, но приходи ещё! ")
    await callback.answer()


@router.callback_query(lambda c: c.data == "about")
async def about_handler(callback: types.CallbackQuery):
    await callback.message.answer(bot_about)
    await callback.answer()


@router.callback_query(lambda c: c.data == "fact")
async def random_fact(callback: types.CallbackQuery):
    await callback.message.answer("🎲 Генерирую факт...")

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты рассказываешь короткие, интересные и необычные факты"
                },
                {
                    "role": "user",
                    "content": "Расскажи один случайный интересный факт"
                }
            ],
        )

        fact = response.choices[0].message.content

        await callback.message.answer(f"🧠 {fact}")

    except Exception as e:
        print("GPT error:", e)
        await callback.message.answer("Ошибка при получении факта 😢")

    await callback.answer()

