import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from parser import parse_ned_kg

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

user_index = {}

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("Привет! Напиши /show чтобы увидеть квартиры.")

@dp.message_handler(commands=["show"])
async def show_cmd(message: types.Message):
    user_id = message.from_user.id
    user_index[user_id] = 0

    listings = parse_ned_kg()
    if not listings:
        await message.answer("Объявления не найдены.")
        return

    await send_listing(message.chat.id, listings[0])

@dp.callback_query_handler(lambda c: c.data in ["like", "next"])
async def callbacks(call: types.CallbackQuery):
    user_id = call.from_user.id
    listings = parse_ned_kg()
    idx = user_index.get(user_id, 0)

    if call.data == "like":
        await bot.answer_callback_query(call.id, "Спасибо! Контакт владельца отправлен в личку.")
    elif call.data == "next":
        idx += 1
        if idx >= len(listings):
            await bot.send_message(call.message.chat.id, "Это были все квартиры.")
            return
        user_index[user_id] = idx
        await send_listing(call.message.chat.id, listings[idx])

def get_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("👍 Нравится", callback_data="like"),
        InlineKeyboardButton("👎 Дальше", callback_data="next")
    )
    return kb

async def send_listing(chat_id, listing):
    caption = (
        f"🏠 <b>{listing['title']}</b>\n"
        f"💰 {listing['price']}\n"
        f"📄 {listing['desc']}\n"
        f"🔗 <a href='{listing['link']}'>Смотреть</a>"
    )
    await bot.send_photo(chat_id, photo=listing['image'], caption=caption, reply_markup=get_keyboard(), parse_mode="HTML")

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
