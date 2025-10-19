import os
import sqlite3
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start
async def start(message: Message):
    await message.reply("Привет! Бот работает ✅")

# /all
async def all_payments(message: Message):
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, amount, description, date FROM payments ORDER BY date DESC LIMIT 20"
    )
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

# Регистрируем хэндлеры через фильтры Command
dp.message.register(start, Command(commands=["start"]))
dp.message.register(all_payments, Command(commands=["all"]))

# Запуск бота через asyncio
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
