import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from os import getenv
from Utils.keyboard import main_keyboard
from Utils.Buttons import router
import asyncio
from dotenv import load_dotenv
from Utils.Buttons import router as buttons_router
from Utils.gpt import router as gpt_router
from Utils.person import router as person_router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)

dp = Dispatcher()
dp.include_router(buttons_router)
dp.include_router(person_router)
dp.include_router(gpt_router)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Нажми кнопку 👇",
        reply_markup=main_keyboard()
    )


async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())