# bot.py
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
import asyncio
from Admin.settings import TOKEN
BOT_TOKEN = TOKEN# export BOT_TOKEN="123:ABC..."

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    # Web App tugmasi — userni webview sahifasiga yuboradi
    web_btn = KeyboardButton(text="Open web view", web_app=WebAppInfo(url="https://www.akmalfarm.uz"))
    kb = ReplyKeyboardMarkup(keyboard=[[web_btn]], resize_keyboard=True)
    await message.answer("Web view demo. Tugmani bosing va ma'lumot yuboring.", reply_markup=kb)

@dp.message()
async def all_messages(message: types.Message):
    # Telegram bot API orqali web appdan kelgan ma'lumot message.web_app_data ichida bo'ladi
    web_data = getattr(message, "web_app_data", None)
    if web_data and getattr(web_data, "data", None):
        # web_data.data — string (odatda JSON)
        await message.answer(f"WebAppdan kelgan ma'lumot:\n{web_data.data}")
    else:
        # oddiy matn xabarlari ham ishlaydi
        await message.answer("Qabul qilindi: " + (message.text or "<no text>"))

if __name__ == "__main__":
    print("Bot polling boshlanmoqda...")
    asyncio.run(dp.start_polling(bot))
