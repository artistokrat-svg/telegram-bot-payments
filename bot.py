import os
import asyncio
import sqlite3
from datetime import datetime
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Бот работает ✅")

@dp.message_handler(commands=['all'])
async def all_payments(message: types.Message):
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, amount, description, date FROM payments ORDER BY date DESC LIMIT 20")
    records = cursor.fetchall()
    conn.close()

    if not records:
        await message.reply("Пока нет поступлений 💸")
        return

    total_sum = sum([r[1] for r in records])
    text = "📊 *Последние поступления:*\n\n"
    for username, amount, description, date in records:
        text += f"👤 {username or 'неизвестно'} — {amount} ₽ — {description or 'без описания'} — {date}\n"
    text += f"\n💰 *Итого за последние операции:* {total_sum} ₽"
    await message.reply(text, parse_mode="Markdown")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
