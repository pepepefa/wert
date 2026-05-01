import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8673993910:AAGWHrU6BnrT75amjCUoGAdfrgfod7nJ-ks"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- DB ---
conn = sqlite3.connect("stats.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    score INTEGER DEFAULT 0
)
""")
conn.commit()


def add_777(user_id, username):
    cur.execute("SELECT score FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()

    if row:
        cur.execute(
            "UPDATE users SET score = score + 1, username = ? WHERE user_id = ?",
            (username, user_id)
        )
    else:
        cur.execute(
            "INSERT INTO users (user_id, username, score) VALUES (?, ?, 1)",
            (user_id, username)
        )
    conn.commit()


# --- /top ---
@dp.message(Command("top"))
async def top(message: types.Message):
    cur.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 10")
    rows = cur.fetchall()

    if not rows:
        await message.answer("Пока нет статистики 😢")
        return

    text = "🏆 Тир-лист по 777:\n\n"
    for i, (username, score) in enumerate(rows, 1):
        text += f"{i}. {username or 'unknown'} — {score}\n"

    await message.answer(text)


# --- пример триггера (ты сам подставишь условие) ---
@dp.message()
async def catch_all(message: types.Message):
    user = message.from_user
    text = message.text or ""

    # 🔥 ВАЖНО: тут ты задаёшь условие "выбивания 777"
    if "777" in text:
        add_777(user.id, user.username or user.first_name)
        await message.answer("🎰 +1 к 777!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
