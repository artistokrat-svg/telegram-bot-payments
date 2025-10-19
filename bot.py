import os
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хэндлер /start
async def start(message: Message):
    await message.reply("Привет! Бот работает ✅")

# Хэндлер /all
async def all_payments(message: Message):
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

# Регистрируем хэндлеры через dp.message.register
dp.message.register(start, commands=["start"])
dp.message.register(all_payments, commands=["all"])

if __name__ == "__main__":
    executor.start_polling(dp, bot)
