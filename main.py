import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "Привет! Я помогу с недвижимостью.\n\n"
        "Выбери действие:\n"
        "1️⃣ Хочу продать квартиру\n"
        "2️⃣ Хочу купить квартиру\n"
        "3️⃣ Хочу узнать про документы и сделки\n"
        "4️⃣ Хочу сдать квартиру\n"
        "5️⃣ Хочу снять квартиру"
    )
    await message.answer(text)

@dp.message()
async def echo_all(message: types.Message):
    await message.answer("Спасибо за сообщение. Мы свяжемся с вами.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
