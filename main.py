import os
import asyncio
from aiogram import Bot, Dispatcher, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("Укажите переменную окружения BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.bot = bot

@dp.message(commands=["start"])
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
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()

if __name__ == "__mai
