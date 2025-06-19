import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

PORT = int(os.getenv("PORT", 8000))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Бот работает.")

async def on_startup(app):
    # Запускаем polling бота в фоне при старте веб-сервера
    asyncio.create_task(dp.start_polling(bot))

async def handle_root(request):
    return web.Response(text="Bot is running")

app = web.Application()
app.router.add_get("/", handle_root)
app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, port=PORT)
